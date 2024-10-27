import tkinter as tk
from tkinter import filedialog, Toplevel
from PIL import Image, ImageTk
import io

def open_size_change(root):
    new_window = Toplevel(root)
    new_window.title("PYIMGM")
    new_window.geometry("500x500")

    title_label = tk.Label(new_window, text="이미지 크기 변경", font=("bold", 10))
    title_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)

    # 새 창의 레이아웃을 설정 (grid 사용)
    new_window.grid_rowconfigure(0, weight=0)  # 제목
    new_window.grid_rowconfigure(1, weight=1)  # 이미지가 중간에 위치
    new_window.grid_rowconfigure(2, weight=0)  # 버튼이 하단에 위치
    new_window.grid_columnconfigure(0, weight=1)  # 버튼과 이미지 중앙 정렬

    # 이미지 라벨을 새 창에서 초기화 (이미지가 표시될 자리)
    img_label = tk.Label(new_window)
    img_label.grid(row=1, column=0, padx=20, pady=20)  # 이미지를 중간에 표시

    def open_image():
        file_path = filedialog.askopenfilename(parent=new_window, filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            load_image(file_path)

    def load_image(file_path):
        # 원본 이미지 로드 및 표시
        img = Image.open(file_path)
        img.thumbnail((300, 300))
        img_tk = ImageTk.PhotoImage(img)
        img_label.config(image=img_tk)  # 이미지를 같은 위치에 표시
        img_label.image = img_tk
        img_label.file_path = file_path  # 이미지 파일 경로 저장

    def resize_image(input_image, width):
        # 이미지의 비율에 맞춰 높이를 조정
        aspect_ratio = input_image.height / input_image.width
        new_height = int(width * aspect_ratio)
        resized_image = input_image.resize((width, new_height), Image.LANCZOS)
        return resized_image

    def change_size():
        # 사이즈 변경 수행
        if hasattr(img_label, 'file_path'):
            input_image = Image.open(img_label.file_path)
            width = int(size_entry.get())  # 입력된 너비 가져오기
            resized_image = resize_image(input_image, width)  # 이미지 크기 조정

            # 결과 이미지 표시
            resized_image.thumbnail((300, 300))  # 썸네일 크기로 조정
            resized_img_tk = ImageTk.PhotoImage(resized_image)
            
            img_label.config(image=resized_img_tk)  # 같은 위치에서 결과 이미지 표시
            img_label.image = resized_img_tk

    def save_image():
        # 저장 수행
        if hasattr(img_label, 'file_path'):
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if file_path:
                output_image = Image.open(img_label.file_path)  # 저장할 이미지 열기
                output_image.save(file_path)  # 지정된 경로에 저장
                print("저장 완료")
        else:
            print("먼저 이미지를 열어야 합니다.")  # 이미지가 없을 경우 처리

    # 이미지 열기 버튼
    open_button = tk.Button(new_window, text="이미지 열기", command=open_image)
    open_button.grid(row=0, column=0, pady=10)

    # 사이즈 입력을 위한 입력 창
    size_entry = tk.Entry(new_window)
    size_entry.grid(row=2, column=0, padx=10, pady=10)
    size_entry.insert(0, "가로 입력")  # 기본 텍스트 설정

    button_frame = tk.Frame(new_window)
    button_frame.grid(row=3, column=0, pady=20)

    # 사이즈 변경 버튼
    change_size_button = tk.Button(button_frame, text="사이즈 변경", command=change_size)
    change_size_button.pack(side="left", padx=10)

    # 이미지 저장 버튼
    save_button = tk.Button(button_frame, text="이미지 저장", command=save_image)
    save_button.pack(side="left", padx=10)
