import requests
import re
import tkinter as tk
from tkinter import messagebox


def get_video_details(video_url):
    """Fetch video details using a regular expression to scrape video title and views."""
    video_id = video_url.split("v=")[-1]
    youtube_url = f"https://www.youtube.com/watch?v={video_id}"

    try:
        # Make a request to the YouTube page to get raw HTML
        response = requests.get(youtube_url)

        if response.status_code == 200:
            # Search for the title and views using regex
            title_match = re.search(r'<title>(.*?)</title>', response.text)
            views_match = re.search(r'viewCount":"(\d+)"', response.text)

            if title_match and views_match:
                title = title_match.group(1)
                views = views_match.group(1)
                return title, views
            else:
                messagebox.showerror("Error", "Could not retrieve video details.")
                return None, None
        else:
            messagebox.showerror("Error", "Failed to fetch video data.")
            return None, None
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return None, None


def show_video_details():
    """Show video details in the GUI."""
    video_url = video_url_entry.get()
    if video_url:
        title, views = get_video_details(video_url)
        if title:
            result_label.config(text=f"Title: {title}\nViews: {views}")
        else:
            result_label.config(text="Video details could not be fetched.")
    else:
        messagebox.showerror("Error", "Please enter a valid YouTube URL.")


# GUI Setup
root = tk.Tk()
root.title("Bukhari Watch Time Tool")
root.geometry("500x300")

header_label = tk.Label(root, text="Bukhari Watch Time", font=("Helvetica", 16, "bold"))
header_label.pack(pady=10)

video_url_label = tk.Label(root, text="Enter YouTube Video URL:")
video_url_label.pack(pady=5)

video_url_entry = tk.Entry(root, width=50)
video_url_entry.pack(pady=5)

fetch_button = tk.Button(root, text="Fetch Video Details", command=show_video_details, width=20)
fetch_button.pack(pady=10)

result_label = tk.Label(root, text="Video details will be shown here.", font=("Helvetica", 12))
result_label.pack(pady=10)

exit_button = tk.Button(root, text="Exit", command=root.quit, width=20)
exit_button.pack(pady=10)

root.mainloop()
