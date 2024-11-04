import tkinter as tk
from tkinter import filedialog, Toplevel, messagebox
from PIL import Image, ImageTk
from moviepy.editor import VideoFileClip

def open_video_to_gif(root):
    new_window = Toplevel(root)
    new_window.title("PYIMGM")
    new_window.geometry("500x600")

    title_label = tk.Label(new_window, text="영상 GIF 변환", font=("bold", 12))
    title_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)

    # new_window grid
    new_window.grid_rowconfigure(0, weight=0)  # title
    new_window.grid_rowconfigure(1, weight=1)  # image
    new_window.grid_rowconfigure(2, weight=0)  # button
    new_window.grid_columnconfigure(0, weight=1)  # button

    video_path = None
    gif_clip = None
    video_label = tk.Label(new_window, text="동영상 파일: 없음")
    video_label.grid(row=1, column=0, padx=10, pady=10)

    def load_video():
        nonlocal video_path
        video_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.mov;*.avi;*.mkv")])
        if video_path:
            video_label.config(text=f"동영상 파일: {video_path.split('/')[-1]}")

    def convert_to_gif():
        nonlocal gif_clip
        if not video_path:
            messagebox.showwarning("경고", "동영상을 먼저 불러와야 합니다.")
            return

        try:
            start_time = float(start_time_entry.get())
            end_time = float(end_time_entry.get())
        except ValueError:
            messagebox.showerror("오류", "시작 시간과 종료 시간을 올바른 숫자로 입력하세요.")
            return

        # make video clip & change to gif(Save to memory only)
        try:
            gif_clip = VideoFileClip(video_path).subclip(start_time, end_time)
            messagebox.showinfo("완료", "GIF로 변환되었습니다. 이제 저장할 수 있습니다.")
        except Exception as e:
            messagebox.showerror("오류", f"GIF 변환 중 오류가 발생했습니다: {e}")

    def save_gif():
        # check gif_clip existed
        if gif_clip is None:
            messagebox.showwarning("경고", "먼저 GIF로 변환해 주세요.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".gif", filetypes=[("GIF files", "*.gif")],
                                                 initialfile="output.gif")
        if save_path:
            try:
                gif_clip.write_gif(save_path, fps=10)  # save GIF (fps=10)
                messagebox.showinfo("완료", f"GIF로 저장되었습니다: {save_path}")
            except Exception as e:
                messagebox.showerror("오류", f"GIF 저장 중 오류가 발생했습니다: {e}")

    # load_video_button
    load_video_button = tk.Button(new_window, text="동영상 불러오기", command=load_video)
    load_video_button.grid(row=2, column=0, pady=10)

    # (start time + start entry) frame
    start_time_frame = tk.Frame(new_window)
    start_time_frame.grid(row=3, column=0, pady=10)

    start_time_label = tk.Label(start_time_frame, text="시작 시간 (초):")
    start_time_label.pack(side="left", padx=5)

    start_time_entry = tk.Entry(start_time_frame, width=10)
    start_time_entry.pack(side="left")

    # (end_time + end entry) frame
    end_time_frame = tk.Frame(new_window)
    end_time_frame.grid(row=4, column=0, pady=10)

    end_time_label = tk.Label(end_time_frame, text="종료 시간 (초):")
    end_time_label.pack(side="left", padx=5)

    end_time_entry = tk.Entry(end_time_frame, width=10)
    end_time_entry.pack(side="left")

    # GIF convert & GIF save frame
    button_frame = tk.Frame(new_window)
    button_frame.grid(row=5, column=0, pady=10)

    # GIF convert
    convert_button = tk.Button(button_frame, text="GIF 변환", command=convert_to_gif)
    convert_button.pack(side="left", padx=10)

    # GIF save
    save_button = tk.Button(button_frame, text="GIF 저장", command=save_gif)
    save_button.pack(side="left", padx=10)
