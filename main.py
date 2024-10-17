import tkinter as tk
from tkinter import filedialog, Toplevel
from PIL import Image, ImageTk
import io
from bg_remove import BackgroundRemover


def dummy_function():
    pass

def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        load_image(file_path)

def load_image(file_path):
    img = Image.open(file_path)
    img.thumbnail((300, 300))
    img_tk = ImageTk.PhotoImage(img)
    label.config(image=img_tk)
    label.image = img_tk
    label.file_path = file_path

def show_full_image(event):
    img = Image.open(label.file_path)
    img_width, img_height = img.size
    new_window = Toplevel(root)
    new_window.title("전체 이미지")
    new_window.geometry(f"{img_width}x{img_height}")
    img_tk = ImageTk.PhotoImage(img)
    full_image_label = tk.Label(new_window, image=img_tk)
    full_image_label.image = img_tk
    full_image_label.pack()

root = tk.Tk()
root.title("PYIMGM")
root.geometry("500x500")

# 그리드를 전체적으로 확장해서 중앙에 배치할 수 있는 여유 공간 확보
root.grid_rowconfigure(0, weight=1)  # 상단 여백
root.grid_rowconfigure(3, weight=1)  # 하단 여백
root.grid_columnconfigure(0, weight=1)  # 좌측 여백
root.grid_columnconfigure(4, weight=1)  # 우측 여백


buttons = [
    tk.Button(root, text="이미지 배경 투명화", command=BackgroundRemover.remove_background, width = 20, height= 2),
    tk.Button(root, text="이미지 외곽선 추출", command=dummy_function, width = 20, height= 2),
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

# open_button = tk.Button(root, text="이미지 열기", command=open_image)
# open_button.pack()

# remove_bg_button = tk.Button(root, text="배경 제거", command=remove_background)
# remove_bg_button.place(x=220, y=500)

# label = tk.Label(root)
# label.pack()

# label.bind("<Button-1>", show_full_image)

root.mainloop()
