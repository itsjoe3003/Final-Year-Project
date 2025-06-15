import tkinter as tk
import vlc
from tkinter import ttk

class VLCPlayer:
    def __init__(self, master):
        self.instance = vlc.Instance("--no-xlib", "--no-video-title-show", "--disable-screensaver", "--quiet", "--file-logging", "--logfile=vlc-log.txt")
        self.player = self.instance.media_player_new()
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

        self.vlc_player_frame = ttk.Frame(master)
        self.vlc_player_frame.pack(fill=tk.BOTH, expand=True)

        self.player.set_hwnd(self.vlc_player_frame.winfo_id())

        self.play_button = ttk.Button(master, text="Play", command=self.play)
        self.play_button.pack(side=tk.LEFT)

        self.pause_button = ttk.Button(master, text="Pause", command=self.pause)
        self.pause_button.pack(side=tk.LEFT)

        self.forward_button = ttk.Button(master, text="Forward 5s", command=lambda: self.navigate(5))
        self.forward_button.pack(side=tk.LEFT)

        self.backward_button = ttk.Button(master, text="Backward 5s", command=lambda: self.navigate(-5))
        self.backward_button.pack(side=tk.LEFT)

        self.timeline = ttk.Scale(master, from_=0, to=100, orient=tk.HORIZONTAL, length=600, command=self.update_timeline)
        self.timeline.pack(pady=10)

        self.master.after(100, self.update_timeline_periodic)



        self.video_paths = {
            "Video 1": r"D:\\FYP\\videos\\Video 1.mp4",
            "Video 2": r"D:\\FYP\\videos\\Video 2.mp4",
            "Video 3": r"D:\\FYP\\videos\\Video 3.mp4",
        }

        self.selected_video = tk.StringVar(master)
        self.video_links = {}
        for title in self.video_paths:
            link = ttk.Label(master, text=title, cursor="hand2")
            link.pack(side=tk.LEFT, padx=10)
            link.bind("<Button-1>", lambda event, title=title: self.load_selected_video(title))

            self.video_links[title] = link

    def play(self):
        self.player.play()

    def pause(self):
        self.player.pause()

    def navigate(self, seconds):
        current_time = self.player.get_time()
        new_time = current_time + seconds * 1000
        self.player.set_time(new_time)
        self.update_timeline(new_time)

    def load_selected_video(self, selected_title):
        video_path = self.video_paths[selected_title]
        self.load_video(video_path)

    def load_video(self, video_path):
        self.player.stop()
        media = self.instance.media_new(video_path)
        self.player.set_media(media)
        self.player.play()

    def on_close(self):
        self.player.stop()
        self.master.destroy()

    def update_timeline(self, value):
        
        try:
            duration = float(self.player.get_length())
            new_time = int(float(value) * duration / 100)  
            self.player.set_time(new_time)
        except ValueError:
            pass

    def update_timeline_periodic(self):
        duration = self.player.get_length()

        if duration is not None and duration > 0:
            current_time = self.player.get_time()
            position = (current_time / duration) * 100
            self.timeline.set(position)

        self.master.after(100, self.update_timeline_periodic)





if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")

    vlc_player = VLCPlayer(root)

    root.mainloop()
