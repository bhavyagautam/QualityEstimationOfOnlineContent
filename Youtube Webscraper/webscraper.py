# video_url = 'https://www.youtube.com/watch?v=URoVKPVDKPU'
# shorts_url ='https://www.youtube.com/shorts/7N5B2Gga3ts'
import yt_dlp
import re
from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd

def extract_video_id(url):
    # For regular YouTube video URLs
    regex_video = r"watch\?v=([a-zA-Z0-9_-]+)&?"
    match_video = re.search(regex_video, url)
    if match_video:
        return match_video.group(1)

    # For YouTube Shorts URLs
    regex_shorts = r"shorts/([a-zA-Z0-9_-]+)$"
    match_shorts = re.search(regex_shorts, url)
    if match_shorts:
        return match_shorts.group(1)

    return None

def get_metadata(video_url):
    ydl_opts = {'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=False)
        view_count = info_dict.get('view_count')
        likes = info_dict.get('like_count')
        comment_count = info_dict.get('comment_count')
        # print("View Count:", view_count)
        # print("Likes:", likes)
        # print("comment_count",comment_count)

    video_id = extract_video_id(video_url)
    if not video_id:
        print(f"Video ID not found for {video_url}")
        return
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    except:
        print(f"No transcript found for {video_url}\nSkipping it.")
        return None
    transcript_text = ''
    for transcript in transcript_list:
        transcript_text += transcript['text'] + ' '
        transcript_text = transcript_text.replace("\'", "'").replace("\n", " ")
        # transcript_text = ' '.join(html.unescape(transcript['text']) for transcript in transcript_list)
    
    # print("Transcript:", transcript_text)
    return transcript_text, view_count, likes, comment_count

# path_to_data = '../Datasets/TED-ED_Youtube_urls.csv'
# path_to_data = '../Datasets/Minecraft_Youtube_urls.csv'
# path_to_data = '../Datasets/mrbeast_youtube_urls.csv'
# path_to_data = '../Datasets/educational_youtube_urls.csv'
path_to_data = '../Datasets/vox_youtube_urls.csv'

dataset = pd.read_csv(path_to_data)

# Initialize lists to store metadata
titles = []
transcripts = []
view_counts = []
comment_counts = []
likes_list = []

# Iterate through each row in the dataset
for index, row in dataset.iterrows():
    # Extract the URL from the second column of the CSV
    video_url = row.iloc[1]

    # Call get_metadata function to retrieve information about the YouTube video
    try:
        metadata = get_metadata(video_url)
        if metadata == None:
            print(f"{index} skipped. Error in metadata")
            continue
    except:
        print(f"Error in getting metadata for {video_url}")
        continue
    transcript, view_count, likes, comment_count = metadata

    # Append metadata to lists
    titles.append(row.iloc[0])
    transcripts.append(transcript)
    view_counts.append(view_count)
    comment_counts.append(comment_count)
    likes_list.append(likes)
    print(f"{index} done")
# Create a DataFrame with the collected metadata
metadata_df = pd.DataFrame({
    'title': titles,
    'transcript': transcripts,
    'view_count': view_counts,
    'comment_count': comment_counts,
    'like_count': likes_list
})
# print(metadata_df['Transcript'])

# Save DataFrame to a CSV file
# metadata_df.to_csv('../Datasets/TED-ED_youtube_metadata.csv', index=False)
# metadata_df.to_csv('../Datasets/minecraft_youtube_metadata.csv', index=False)
# metadata_df.to_csv('../Datasets/mrbeast_youtube_metadata.csv', index=False)
# metadata_df.to_csv('../Datasets/educational_youtube_metadata.csv', index=False)
metadata_df.to_csv('../Datasets/vox_youtube_metadata.csv', index=False)
