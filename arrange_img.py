import tkinter as tk
from tkinter import filedialog, Toplevel, messagebox
from PIL import Image, ImageTk

def open_multiple_images(root):
    new_window = Toplevel(root)
    new_window.title("여러 이미지 크기 변경")
    new_window.geometry("600x600")

    title_label = tk.Label(new_window, text="여러 이미지 크기 변경", font=("bold", 12))
    title_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)

    img_display = tk.Label(new_window)
    img_display.grid(row=1, column=0, padx=20, pady=20)

    image_paths = []  # 불러온 이미지 파일 경로 저장
    image_listbox = tk.Listbox(new_window, width=50, height=10)
    image_listbox.grid(row=2, column=0, padx=20, pady=10)

    def load_images():
        file_paths = filedialog.askopenfilenames(parent=new_window, filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_paths:
            for file_path in file_paths:
                image_paths.append(file_path)
                image_listbox.insert(tk.END, file_path.split("/")[-1])  # 파일 이름 추가

    def resize_images():
        if not image_paths:
            messagebox.showwarning("경고", "이미지를 먼저 불러와야 합니다.")
            return

        try:
            target_width = int(size_entry.get())  # 입력된 가로 크기 가져오기
        except ValueError:
            messagebox.showerror("오류", "유효한 숫자를 입력하세요.")
            return

        resized_images = []

        for path in image_paths:
            img = Image.open(path)
            aspect_ratio = img.height / img.width
            new_height = int(target_width * aspect_ratio)
            resized_image = img.resize((target_width, new_height), Image.LANCZOS)
            resized_images.append(resized_image)

        save_resized_images(resized_images)

    def save_resized_images(resized_images):
        for i, resized_image in enumerate(resized_images):
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")],
                                                      initialfile=f"resized_image_{i + 1}.png")
            if save_path:
                resized_image.save(save_path)
                print(f"저장 완료: {save_path}")

    # 이미지 열기 버튼
    open_button = tk.Button(new_window, text="이미지 열기", command=load_images)
    open_button.grid(row=0, column=0, pady=10)

    # 가로 크기 입력 필드
    size_entry = tk.Entry(new_window)
    size_entry.grid(row=3, column=0, padx=10, pady=10)
    size_entry.insert(0, "가로 크기 입력")  # 기본 텍스트 설정

    # 사이즈 변경 버튼
    resize_button = tk.Button(new_window, text="사이즈 변경", command=resize_images)
    resize_button.grid(row=4, column=0, pady=10)

# 메인 GUI 코드
root = tk.Tk()
root.title("이미지 처리 프로그램")
root.geometry("300x200")

open_images_button = tk.Button(root, text="여러 이미지 크기 변경", command=lambda: open_multiple_images(root))
open_images_button.pack(pady=20)

root.mainloop()
