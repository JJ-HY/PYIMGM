import tkinter as tk
from tkinter import filedialog, Toplevel
from PIL import Image, ImageTk
from rembg import remove
import io
import cv2
import numpy as np


def open_contour_find(root):
    new_window = Toplevel(root)
    new_window.title("PYIMGM")
    new_window.geometry("500x500")

    title_label = tk.Label(new_window, text="이미지 외곽선 추출", font=("bold", 10))
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

    def find_contour():
        # 이미지 읽어오기
        if hasattr(img_label, 'file_path'):
            img = cv2.imread(img_label.file_path)  # img_label에서 파일 경로를 가져옴

            # 이미지를 grayscale로 변환
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # 이미지 이진화
            _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

            # 윤곽선 검출
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # 검은색 배경 이미지 생성
            contour_img = np.zeros_like(img)  # 윤곽선 이미지를 위한 빈 배열

            # 윤곽선을 검은색으로 그리기
            cv2.drawContours(contour_img, contours, -1, (255, 255, 255), 2)  # 외곽선 그리기 (흰색)

            # OpenCV 이미지를 PIL로 변환
            img_rgb = cv2.cvtColor(contour_img, cv2.COLOR_BGR2RGB)  # BGR에서 RGB로 변환
            img_pil = Image.fromarray(img_rgb)  # numpy 배열을 PIL 이미지로 변환

            # 이미지를 Tkinter의 Label에 표시
            img_tk = ImageTk.PhotoImage(img_pil)  # PIL 이미지를 Tkinter 이미지로 변환
            img_label.config(image=img_tk)  # Label에 이미지 설정
            img_label.image = img_tk  # 가비지 컬렉션 방지를 위한 참조 저장
        else:
            print("먼저 이미지를 열어야 합니다.")  # 이미지가 없을 경우 메시지 표시



    def save_image():
        # 저장 수행
        if hasattr(img_label, 'file_path'):
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if file_path:
                output_image = Image.open(img_label.file_path)  # 저장할 이미지 열기
                output_image.save(file_path)  # 지정된 경로에 저장
                print("저장 완료")
        else:
            print("먼저 기능을 수행해야 합니다.")

    # 이미지 열기 버튼
    open_button = tk.Button(new_window, text="이미지 열기", command=open_image)
    open_button.grid(row=0, column=0, pady=10)

    button_frame = tk.Frame(new_window)
    button_frame.grid(row=2, column=0, pady=20)

    # 이미지 외곽 추출 버튼
    find_contour_button = tk.Button(button_frame, text="이미지 외곽선 추출", command=find_contour)
    find_contour_button.pack(side="left", padx=10)

    # 이미지 저장 버튼
    save_button = tk.Button(button_frame, text="이미지 저장", command=save_image)
    save_button.pack(side="left", padx=10)

