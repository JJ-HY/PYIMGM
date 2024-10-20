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

    def remove_background():
        # 배경 제거 수행
        if hasattr(img_label, 'file_path'):
            input_image = Image.open(img_label.file_path)
            output_image = remove(input_image)

            # 결과 이미지를 메모리에 저장
            img_byte_arr = io.BytesIO()
            output_image.save(img_byte_arr, format='PNG')  # 'format' 오타 수정
            img_byte_arr = img_byte_arr.getvalue()

            # 결과 이미지 표시
            result_img = Image.open(io.BytesIO(img_byte_arr))
            result_img.thumbnail((300, 300))
            result_img_tk = ImageTk.PhotoImage(result_img)
            
            img_label.config(image=result_img_tk)  # 같은 위치에서 결과 이미지 표시
            img_label.image = result_img_tk

            # # 결과 이미지 저장
            # output_path = img_label.file_path.rsplit('.', 1)[0] + '_nobg.png'
            # output_image.save(output_path)  # 수정된 결과 이미지 저장
            # img_label.file_path = output_path  # 새로운 파일 경로 저장

    def save_image():
        # 저장 수행
        if hasattr(img_label, 'file_path'):
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if file_path:
                output_image = Image.open(img_label.file_path)  # 저장할 이미지 열기
                output_image.save(file_path)  # 지정된 경로에 저장
                print("저장 완료")
        else:
            print("먼저 이미지를 열어야 합니다.")  # 배경 제거가 안 됐을 경우 처리

    # 이미지 열기 버튼
    open_button = tk.Button(new_window, text="이미지 열기", command=open_image)
    open_button.grid(row=0, column=0, pady=10)

    button_frame = tk.Frame(new_window)
    button_frame.grid(row=2, column=0, pady=20)

    # 배경 제거 버튼
    remove_bg_button = tk.Button(button_frame, text="배경 제거", command=remove_background)
    remove_bg_button.pack(side="left", padx=10)

    # 이미지 저장 버튼
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
