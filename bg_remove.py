import tkinter as tk
from tkinter import filedialog, Toplevel
from PIL import Image, ImageTk
from rembg import remove
import io

def open_bg_remove(root):
    new_window = Toplevel(root)
    new_window.title("PYIMGM")
    new_window.geometry("500x500")

    title_label = tk.Label(new_window, text="이미지 배경 투명화", font=("bold", 10))
    title_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)

    # new_window grid
    new_window.grid_rowconfigure(0, weight=0)  # title
    new_window.grid_rowconfigure(1, weight=1)  # image
    new_window.grid_rowconfigure(2, weight=0)  # button
    new_window.grid_columnconfigure(0, weight=1)  # button

    # img label
    img_label = tk.Label(new_window)
    img_label.grid(row=1, column=0, padx=20, pady=20)  

    def open_image():
        file_path = filedialog.askopenfilename(parent=new_window, filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            load_image(file_path)

    def load_image(file_path):
        # original img
        img = Image.open(file_path)
        img.thumbnail((300, 300))
        img_tk = ImageTk.PhotoImage(img)
        img_label.config(image=img_tk)  # same location img
        img_label.image = img_tk
        img_label.file_path = file_path  # save file_path

    def remove_background():
        # remove bg
        if hasattr(img_label, 'file_path'):
            input_image = Image.open(img_label.file_path)
            output_image = remove(input_image)

            # save img_byte_arr
            img_byte_arr = io.BytesIO()
            output_image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()

            # Display result image
            result_img = Image.open(io.BytesIO(img_byte_arr))
            result_img.thumbnail((300, 300))
            result_img_tk = ImageTk.PhotoImage(result_img)
            
            img_label.config(image=result_img_tk)
            img_label.image = result_img_tk
            img_label.output_image = output_image  # Store the img for saving

    def save_image():
        # save
        if hasattr(img_label, 'output_image'):
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if file_path:
                img_label.output_image.save(file_path)
                print("저장 완료")
        else:
            print("배경을 먼저 제거해주세요.")

    # open img button
    open_button = tk.Button(new_window, text="이미지 열기", command=open_image)
    open_button.grid(row=0, column=0, pady=10)

    button_frame = tk.Frame(new_window)
    button_frame.grid(row=2, column=0, pady=20)

    # rembg button
    remove_bg_button = tk.Button(button_frame, text="배경 제거", command=remove_background)
    remove_bg_button.pack(side="left", padx=10)

    # save button
    save_button = tk.Button(button_frame, text="이미지 저장", command=save_image)
    save_button.pack(side="left", padx=10)

# class BackgroundRemover:
#     def __init__(self, file_path):
#         self.file_path = file_path
#         self.input_image = Image.open(file_path)
#         self.output_image = None

#     def remove_background(self):
#         # 배경 제거
#         self.output_image = remove(self.input_image)
#         return self.output_image

#     def save_image(self):
#         if self.output_image is None:
#             raise ValueError("배경이 제거된 이미지가 없습니다.")
        
#         # 결과 이미지를 메모리에 저장
#         img_byte_arr = io.BytesIO()
#         self.output_image.save(img_byte_arr, format='PNG')
#         return img_byte_arr.getvalue()
