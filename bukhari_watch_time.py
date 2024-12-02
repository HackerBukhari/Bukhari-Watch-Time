import tkinter as tk
from tkinter import messagebox
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import random
import time
import threading

# YouTube API setup
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def authenticate_youtube():
    """Authenticate to YouTube API."""
    creds = None
    # Load credentials if available (replace with your own credentials logic)
    if creds and creds.valid:
        return build("youtube", "v3", credentials=creds)
    else:
        messagebox.showerror("Error", "Unable to authenticate with YouTube API. Please check your credentials.")
        return None

def get_video_details(video_url):
    """Fetch video details using YouTube API."""
    video_id = video_url.split("v=")[-1]
    youtube = authenticate_youtube()
    if youtube:
        request = youtube.videos().list(part="snippet,statistics", id=video_id)
        response = request.execute()
        
        if 'items' in response:
            video_data = response["items"][0]["snippet"]
            title = video_data["title"]
            description = video_data["description"]
            tags = video_data.get("tags", [])
            return title, description, tags
        else:
            messagebox.showerror("Error", "Video not found.")
            return None, None, None
    else:
        return None, None, None

def get_watch_time(video_url):
    """Fetch watch time for the video."""
    video_id = video_url.split("v=")[-1]
    youtube = authenticate_youtube()
    if youtube:
        request = youtube.videos().list(part="statistics", id=video_id)
        response = request.execute()

        if 'items' in response:
            views = int(response["items"][0]["statistics"]["viewCount"])
            return views
        else:
            messagebox.showerror("Error", "Video not found.")
            return None
    else:
        return None

def optimize_video_title(title):
    """Suggest title optimizations based on trends."""
    common_keywords = ["how to", "guide", "tutorial", "tips", "best"]
    optimized_title = random.choice(common_keywords) + " " + title
    return optimized_title

def optimize_video_description(description):
    """Suggest description optimizations based on popular descriptions."""
    popular_keywords = ["Learn", "Master", "Complete Guide", "Ultimate"]
    optimized_description = description + " " + random.choice(popular_keywords)
    return optimized_description

def optimize_video_tags(tags):
    """Suggest more relevant tags."""
    common_tags = ["tutorial", "guide", "how to", "tips", "beginner"]
    optimized_tags = list(set(tags + common_tags))
    return optimized_tags

def show_about():
    """Display information about the tool."""
    messagebox.showinfo("About", "This tool helps you optimize and track YouTube videos to increase watch time. It optimizes titles, descriptions, tags, and tracks views.")

def optimize_and_track_video(video_url):
    """Optimize video details and track watch time progress."""
    title, description, tags = get_video_details(video_url)
    
    if title and description:
        optimized_title = optimize_video_title(title)
        optimized_description = optimize_video_description(description)
        optimized_tags = optimize_video_tags(tags)
        
        # Display optimized details
        messagebox.showinfo("Optimized Video Details", f"Optimized Title: {optimized_title}\nOptimized Description: {optimized_description}\nOptimized Tags: {', '.join(optimized_tags)}")
        
        # Track watch time progress in a separate thread for real-time updates
        threading.Thread(target=track_watch_time, args=(video_url,)).start()

    else:
        messagebox.showerror("Error", "Video details could not be fetched.")

def track_watch_time(video_url):
    """Track watch time and update it periodically."""
    while True:
        watch_time = get_watch_time(video_url)
        if watch_time is not None:
            # Update the watch time in real-time
            result_label.config(text=f"Current Watch Time: {watch_time} views")
        time.sleep(30)  # Update every 30 seconds

def show_error_message(message):
    """Show a generic error message."""
    messagebox.showerror("Error", message)

# GUI Setup
root = tk.Tk()
root.title("Bukhari Watch Time")
root.geometry("450x350")
root.resizable(False, False)

header_label = tk.Label(root, text="Bukhari Watch Time", font=("Helvetica", 16, "bold"))
header_label.pack(pady=10)

video_url_label = tk.Label(root, text="Enter YouTube Video URL:")
video_url_label.pack(pady=5)

video_url_entry = tk.Entry(root, width=40)
video_url_entry.pack(pady=5)

optimize_button = tk.Button(root, text="Optimize & Track Video", command=lambda: optimize_and_track_video(video_url_entry.get()), width=30)
optimize_button.pack(pady=10)

result_label = tk.Label(root, text="Current Watch Time: N/A", font=("Helvetica", 12))
result_label.pack(pady=10)

about_button = tk.Button(root, text="About", command=show_about, width=20)
about_button.pack(pady=10)

exit_button = tk.Button(root, text="Exit", command=root.quit, width=20)
exit_button.pack(pady=10)

root.mainloop()
