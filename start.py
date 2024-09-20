import tkinter as tk
from tkinter import filedialog, Toplevel
from PIL import Image, ImageTk
from rembg import remove
import io

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

def remove_background():
    if hasattr(label, 'file_path'):
        input_image = Image.open(label.file_path)
        output_image = remove(input_image)
        
        # 결과 이미지를 메모리에 저장
        img_byte_arr = io.BytesIO()
        output_image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        
        # 결과 이미지 표시
        img = Image.open(io.BytesIO(img_byte_arr))
        img.thumbnail((300, 300))
        img_tk = ImageTk.PhotoImage(img)
        label.config(image=img_tk)
        label.image = img_tk
        
        # 결과 이미지 저장
        # output_path = label.file_path.rsplit('.', 1)[0] + '_nobg.png'
        # output_image.save(output_path)
        # label.file_path = output_path
        
        # print(f"배경이 제거된 이미지가 저장되었습니다: {output_path}")

root = tk.Tk()
root.title("PYIMGM")
root.geometry("500x550+500+150")

open_button = tk.Button(root, text="이미지 열기", command=open_image)
open_button.pack()

remove_bg_button = tk.Button(root, text="배경 제거", command=remove_background)
remove_bg_button.place(x=220, y=500)

label = tk.Label(root)
label.pack()

label.bind("<Button-1>", show_full_image)

root.mainloop()