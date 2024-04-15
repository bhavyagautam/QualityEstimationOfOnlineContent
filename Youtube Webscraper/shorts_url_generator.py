from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import time

options = Options()
options.add_experimental_option("detach",True)

# Set up Chrome WebDriver (you can use other browsers as well)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options=options)

# URL of the YouTube Shorts page
url = "https://www.youtube.com/shorts"
# Open the page
driver.get(url)

# Scroll down to load more videos
SCROLL_PAUSE_TIME = 2

# Get scroll height
last_height = driver.execute_script("return document.documentElement.scrollHeight")

cnt = 0
while True:
    if cnt == 10:
        break
    cnt+=1
    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.documentElement.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

print("Loop Done")

# Close the browser
driver.quit()

