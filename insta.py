import re
import requests
from instaloader import Instaloader, Post

def extract_shortcode(url):
    # Extract the shortcode from the Instagram reel URL
    match = re.search(r'instagram\.com/reel/([A-Za-z0-9_-]+)', url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Invalid Instagram reel URL")

def download_reel(url):
    # Extract the shortcode from the provided URL
    shortcode = extract_shortcode(url)
    
    # Create an Instaloader instance
    L = Instaloader()
    
    # Fetch the post (reel) using the shortcode
    post = Post.from_shortcode(L.context, shortcode)
    
    if post.video_url:
        # Download the video with audio using requests
        video_url = post.video_url
        response = requests.get(video_url, stream=True)
        if response.status_code == 200:
            filename = f"{shortcode}.mp4"
            with open(filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
            print(f"Reel downloaded as {filename}")
        else:
            print("Failed to download the reel. Status code:", response.status_code)
    else:
        print("This is not a video reel.")

if __name__ == "__main__":
    # Ask the user for the Instagram reel URL
    url = input("Enter the Instagram reel URL: ")
    
    try:
        # Call the function to download the reel
        download_reel(url)
    except Exception as e:
        print(f"An error occurred: {e}")
