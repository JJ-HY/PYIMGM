import tkinter as tk
from tkinter import filedialog, Toplevel
from PIL import Image, ImageTk
from rembg import remove
import io

def open_image_in_new_window(root):
    new_window = Toplevel(root)
    new_window.title("이미지 열기")
    new_window.geometry("300x200")

    def open_image():
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            load_image(file_path)

    def load_image(file_path):
        img = Image.open(file_path)
        img.thumbnail((300, 300))
        img_tk = ImageTk.PhotoImage(img)
        
        # 이미지를 새 창에 표시
        img_label = tk.Label(new_window, image=img_tk)
        img_label.image = img_tk  # Reference to avoid garbage collection
        img_label.pack(padx=20, pady=20)

        # 배경 제거 수행
        remover = BackgroundRemover(file_path)
        remover.remove_background()  # 배경 제거 수행
        img_byte_arr = remover.save_image_to_memory()  # 결과 이미지 저장

        # 결과 이미지 표시
        result_img = Image.open(io.BytesIO(img_byte_arr))
        result_img.thumbnail((300, 300))
        result_img_tk = ImageTk.PhotoImage(result_img)
        
        result_label = tk.Label(new_window, image=result_img_tk)
        result_label.image = result_img_tk
        result_label.pack(pady=10)

    # 이미지 열기 버튼
    open_button = tk.Button(new_window, text="이미지 열기", command=open_image)
    open_button.pack(pady=10)

class BackgroundRemover:
    def __init__(self, file_path):
        self.file_path = file_path
        self.input_image = Image.open(file_path)
        self.output_image = None

    def remove_background(self):
        # 배경 제거
        self.output_image = remove(self.input_image)
        return self.output_image

    def save_image_to_memory(self):
        if self.output_image is None:
            raise ValueError("배경이 제거된 이미지가 없습니다. 먼저 remove_background를 호출하십시오.")
        
        # 결과 이미지를 메모리에 저장
        img_byte_arr = io.BytesIO()
        self.output_image.save(img_byte_arr, format='PNG')
        return img_byte_arr.getvalue()
