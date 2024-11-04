import tkinter as tk
from tkinter import filedialog, Toplevel
from PIL import Image, ImageTk
import io
import bg_remove
import contour_find
import gif_bg_remove
import size_change
import arrange_img
import video_gif_change

def dummy_function():
    pass

root = tk.Tk()
root.title("PYIMGM")
root.geometry("500x500")

# grid
root.grid_rowconfigure(0, weight=1)  
root.grid_rowconfigure(3, weight=1)  
root.grid_columnconfigure(0, weight=1)  
root.grid_columnconfigure(4, weight=1)  

buttons = [
    tk.Button(root, text="이미지 배경 투명화", command=lambda: bg_remove.open_bg_remove(root), width=20, height=2),
    tk.Button(root, text="이미지 외곽선 추출", command=lambda: contour_find.open_contour_find(root), width=20, height=2),
    tk.Button(root, text="GIF 배경 투명화", command=lambda: gif_bg_remove.open_gif_transparent(root), width=20, height=2),
    tk.Button(root, text="이미지 사이즈 변환", command=lambda: size_change.open_size_change(root), width=20, height=2),
    tk.Button(root, text="다수 이미지 정렬&합성", command=lambda: arrange_img.open_multiple_images(root), width=20, height=2),
    tk.Button(root, text="영상 GIF 변환", command=lambda: video_gif_change.open_video_to_gif(root), width=20, height=2),
]

# button
for i, button in enumerate(buttons):
    row = i // 2 
    column = i % 2 + 1 
    button.grid(row=row, column=column, padx=10, pady=10)

# exit button
exit_button = tk.Button(root, text="종료", command=root.quit, width=10, height=1)
exit_button.grid(row=3, column=1, columnspan=2)  # 마지막 행 중앙에 위치

# grid configure
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1) 
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

root.mainloop()
