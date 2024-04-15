from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd
# Helper Functions
def get_transcript(video_id):
    if not video_id:
        print(f"Video ID not found for {video_id}")
        return
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    except:
        print(f"No transcript found for {video_id}. Skipping it.")
        return None
    transcript_text = ''
    for transcript in transcript_list:
        transcript_text += transcript['text'] + ' '
        transcript_text = transcript_text.replace("\'", "'").replace("\n", " ")

    return transcript_text
# Loading and manipulating the data for trending youtube videos
category_id_not_include = [
    10, # Music
    30, # Movies
    31, # Anime/Animation
    42, # Shorts
    44, # Trailers
]
yt_data = pd.read_csv("./Datasets/GB_youtube_trending_data.csv")

# Filter out rows with category IDs not included
filtered_data = yt_data[~yt_data['categoryId'].isin(category_id_not_include)]

# Select only the desired columns
new_data = filtered_data[['video_id','title', 'view_count', 'likes', 'dislikes', 'comment_count', 'categoryId']]

# Optionally, reset index if you want a fresh index for the new dataset
new_data.reset_index(drop=True, inplace=True)
new_data = new_data.drop_duplicates(subset=['video_id'])

# Getting the transcript for the videos
new_data['transcript'] = new_data['video_id'].apply(get_transcript)

# Save the new dataset to a CSV file
new_data.to_csv("./Datasets/GB_youtube_filtered_dataset.csv", index=False)