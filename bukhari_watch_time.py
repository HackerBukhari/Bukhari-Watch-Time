import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar

def load_and_analyze_csv():
    """Load a YouTube Analytics CSV file and analyze watch time."""
    file_path = filedialog.askopenfilename(
        filetypes=[("CSV Files", "*.csv")],
        title="Select YouTube Analytics CSV File"
    )

    if not file_path:
        return

    try:
        # Load the CSV file
        data = pd.read_csv(file_path)

        # Check for required columns
        if "Estimated minutes watched" not in data.columns or "Video Title" not in data.columns:
            messagebox.showerror(
                "Invalid File",
                "The selected file must contain 'Estimated minutes watched' and 'Video Title' columns."
            )
            return

        # Perform calculations
        total_minutes = data["Estimated minutes watched"].sum()
        total_hours = total_minutes // 60
        progress = min(total_hours / 4000 * 100, 100)

        # Display results
        progress_bar["value"] = progress
        progress_label.config(text=f"{total_hours}/4000 hours")
        result_label.config(text=f"Total Watch Time: {total_hours} hours")

        # Show top-performing videos
        top_videos = data.nlargest(3, "Estimated minutes watched")[["Video Title", "Estimated minutes watched"]]
        insights = "\n".join(f"- {row['Video Title']}: {row['Estimated minutes watched']} mins" for _, row in top_videos.iterrows())
        messagebox.showinfo("Top Videos", f"Top Performing Videos:\n{insights}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def show_about():
    """Display information about the tool."""
    messagebox.showinfo(
        "About Bukhari Watch Time",
        "This tool helps you analyze YouTube watch time and track progress toward the 4,000-hour monetization goal.\n\nDeveloped for digital agencies."
    )

# GUI Setup
root = tk.Tk()
root.title("Bukhari Watch Time")
root.geometry("400x300")
root.resizable(False, False)

# Header
header_label = tk.Label(root, text="Bukhari Watch Time", font=("Helvetica", 16, "bold"))
header_label.pack(pady=10)

# Upload Button
upload_button = tk.Button(root, text="Upload and Analyze CSV", command=load_and_analyze_csv, width=30)
upload_button.pack(pady=10)

# Progress Bar
progress_bar = Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=10)

progress_label = tk.Label(root, text="0/4000 hours")
progress_label.pack()

# Result Label
result_label = tk.Label(root, text="Total Watch Time: N/A", font=("Helvetica", 12))
result_label.pack(pady=10)

# About Button
about_button = tk.Button(root, text="About", command=show_about, width=20)
about_button.pack(pady=10)

# Exit Button
exit_button = tk.Button(root, text="Exit", command=root.quit, width=20)
exit_button.pack(pady=10)

root.mainloop()
