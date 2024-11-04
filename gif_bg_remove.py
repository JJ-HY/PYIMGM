import tkinter as tk
from tkinter import filedialog, Toplevel
from PIL import Image, ImageTk, ImageSequence
import io
from rembg import remove  # rembg를 사용하여 배경 제거

def open_gif_transparent(root):
    new_window = Toplevel(root)
    new_window.title("PYIMGM")
    new_window.geometry("500x500")

    title_label = tk.Label(new_window, text="GIF 배경 제거", font=("bold", 10))
    title_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)

    # new_window grid
    new_window.grid_rowconfigure(0, weight=0)  # title
    new_window.grid_rowconfigure(1, weight=1)  # image
    new_window.grid_rowconfigure(2, weight=0)  # button
    new_window.grid_columnconfigure(0, weight=1)  # button

    img_label = tk.Label(new_window)
    img_label.grid(row=1, column=0, padx=20, pady=20)  # 이미지를 중간에 표시

    gif_frames = []  # GIF 프레임 저장
    frame_index = 0  # 현재 프레임 인덱스
    animation_running = False  # 애니메이션 상태
    processed_frames = []  # 배경 제거 후의 GIF 프레임 저장

    def open_gif():
        file_path = filedialog.askopenfilename(parent=new_window, filetypes=[("GIF Files", "*.gif")])
        if file_path:
            img_label.file_path = file_path 
            load_gif(file_path)

    def load_gif(file_path):
        nonlocal gif_frames, frame_index, animation_running
        gif_image = Image.open(file_path)

        # 각 프레임을 처리
        gif_frames = [frame.copy() for frame in ImageSequence.Iterator(gif_image)]

        # 첫 번째 프레임 미리보기 이미지로 표시
        img_preview = gif_frames[0].copy()
        img_preview.thumbnail((300, 300))
        img_tk = ImageTk.PhotoImage(img_preview)
        img_label.config(image=img_tk)
        img_label.image = img_tk

        # 애니메이션 준비
        frame_index = 0
        animation_running = True
        play_animation()

    def apply_rembg_to_gif():
        nonlocal processed_frames
        processed_frames = []

        # 각 프레임에 rembg를 적용하여 배경 제거
        for frame in gif_frames:
            # PIL 이미지를 바이트 배열로 변환
            frame_bytes = io.BytesIO()
            frame.save(frame_bytes, format="PNG")
            frame_bytes = frame_bytes.getvalue()

            # rembg를 통해 배경 제거
            result = remove(frame_bytes)

            # 배경 제거된 이미지를 다시 PIL 이미지로 변환
            frame_removed_bg = Image.open(io.BytesIO(result)).convert("RGBA")
            processed_frames.append(frame_removed_bg)

        # 미리보기
        img_preview = processed_frames[0].copy()
        img_preview.thumbnail((300, 300))  # 썸네일 크기로 조정
        img_tk = ImageTk.PhotoImage(img_preview)
        img_label.config(image=img_tk)
        img_label.image = img_tk

    def play_animation():
        nonlocal frame_index, gif_frames
        if animation_running and processed_frames:
            # 배경이 제거된 프레임을 순차적으로 업데이트하여 GIF 애니메이션 재생
            img_tk = ImageTk.PhotoImage(processed_frames[frame_index])
            img_label.config(image=img_tk)
            img_label.image = img_tk  
            frame_index = (frame_index + 1) % len(processed_frames)  # 다음 프레임으로 이동
            new_window.after(100, play_animation)  # 100ms 후에 다음 프레임 업데이트

    # def stop_animation():
    #     nonlocal animation_running
    #     animation_running = False  # 애니메이션 중지

    def save_transparent_gif():
        # 배경 제거된 GIF 저장
        if processed_frames:
            file_path = filedialog.asksaveasfilename(defaultextension=".gif", filetypes=[("GIF files", "*.gif")])
            if file_path:
                # 첫 프레임에서 시작
                processed_frames[0].save(file_path, save_all=True, append_images=processed_frames[1:], loop=0, transparency=0)
                print(f"저장 완료: {file_path}")
        else:
            print("먼저 배경 제거를해야 합니다.")

    # GIF 열기 버튼
    open_button = tk.Button(new_window, text="GIF 열기", command=open_gif)
    open_button.grid(row=0, column=0, pady=10)

    button_frame = tk.Frame(new_window)
    button_frame.grid(row=2, column=0, pady=20)

    # GIF 배경 제거 및 재생 버튼
    transparent_gif_button = tk.Button(button_frame, text="GIF 배경 제거", command=apply_rembg_to_gif)
    transparent_gif_button.pack(side="left", padx=10)

    # GIF 저장 버튼
    save_button = tk.Button(button_frame, text="GIF 저장", command=save_transparent_gif)
    save_button.pack(side="left", padx=10)

    # # 애니메이션 중지 버튼
    # stop_button = tk.Button(button_frame, text="GIF 애니메이션 중지", command=stop_animation)
    # stop_button.pack(side="left", padx=10)
