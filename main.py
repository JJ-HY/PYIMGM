import tkinter as tk
from tkinter import filedialog, Toplevel
from PIL import Image, ImageTk
import io
import bg_remove
import contour_find


def dummy_function():
    pass

root = tk.Tk()
root.title("PYIMGM")
root.geometry("500x500")

# 그리드 배치
root.grid_rowconfigure(0, weight=1)  
root.grid_rowconfigure(3, weight=1)  
root.grid_columnconfigure(0, weight=1)  
root.grid_columnconfigure(4, weight=1)  

buttons = [
    tk.Button(root, text="이미지 배경 투명화", command=lambda: bg_remove.open_bg_remove(root), width=20, height=2),
    tk.Button(root, text="이미지 외곽선 추출", command=lambda: contour_find.open_contour_find(root), width = 20, height= 2),
    tk.Button(root, text="GIF 배경 투명화", command=dummy_function, width = 20, height= 2),
    tk.Button(root, text="이미지 사이즈 변환", command=dummy_function, width = 20, height= 2),
    tk.Button(root, text="다수 이미지 정렬", command=dummy_function, width = 20, height= 2),
    tk.Button(root, text="다수 이미지 합성", command=dummy_function, width = 20, height= 2),
    tk.Button(root, text="영상 GIF 변환", command=dummy_function, width = 20, height= 2),
    tk.Button(root, text="종료", command=root.quit, width = 10, height= 1)
]

# 2열 4행
for i, button in enumerate(buttons):
    row = i // 2 
    column = i % 2 + 1 
    button.grid(row=row, column=column, padx=10, pady=10)

# 여백 추가
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1) 
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

root.mainloop()
