import tkinter as tk
from tkinter import filedialog, Toplevel
from PIL import Image, ImageTk
import cv2
import numpy as np

def open_contour_find(root):
    new_window = Toplevel(root)
    new_window.title("PYIMGM")
    new_window.geometry("500x500")

    title_label = tk.Label(new_window, text="이미지 외곽선 추출", font=("bold", 10))
    title_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)

    new_window.grid_rowconfigure(0, weight=0)  # 제목
    new_window.grid_rowconfigure(1, weight=1)  # 이미지가 중간에 위치
    new_window.grid_rowconfigure(2, weight=0)  # 버튼이 하단에 위치
    new_window.grid_columnconfigure(0, weight=1)  # 버튼과 이미지 중앙 정렬

    img_label = tk.Label(new_window)
    img_label.grid(row=1, column=0, padx=20, pady=20)  # 이미지를 중간에 표시

    contour_image_full = None  # 원본 크기의 외곽선 이미지를 저장할 변수

    def open_image():
        file_path = filedialog.askopenfilename(parent=new_window, filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            load_image(file_path)

    def load_image(file_path):
        # 원본 이미지 로드 및 표시
        img = Image.open(file_path)
        img.thumbnail((300, 300))  # 300x300 크기로 축소하여 표시
        img_tk = ImageTk.PhotoImage(img)
        img_label.config(image=img_tk)  # 이미지를 같은 위치에 표시
        img_label.image = img_tk
        img_label.file_path = file_path  # 이미지 파일 경로 저장

    def find_contour():
        # 이미지 읽어오기
        nonlocal contour_image_full
        if hasattr(img_label, 'file_path'):
            img = cv2.imread(img_label.file_path)

            # 이미지가 정상적으로 로드되었는지 확인
            if img is None:
                print("이미지를 불러오지 못했습니다. 파일 경로를 확인하세요.")
                return  # 이미지 로드 실패 시 함수 종료

            # 이미지를 grayscale로 변환
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # 이미지 이진화
            _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

            # 윤곽선 검출
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # 검은색 배경 이미지 생성
            contour_img = np.zeros_like(img)

            # 윤곽선 그리기
            cv2.drawContours(contour_img, contours, -1, (255, 255, 255), 2)

            # OpenCV 이미지를 PIL로 변환
            img_rgb = cv2.cvtColor(contour_img, cv2.COLOR_BGR2RGB)
            contour_image_full = Image.fromarray(img_rgb)  # 원본 크기의 외곽선 이미지를 저장

            # Tkinter 상에 300x300으로 축소한 이미지 표시
            contour_thumbnail = contour_image_full.copy()
            contour_thumbnail.thumbnail((300, 300))  # 300x300 썸네일로 변환
            img_tk = ImageTk.PhotoImage(contour_thumbnail)
            img_label.config(image=img_tk)  # Label에 축소된 이미지 설정
            img_label.image = img_tk  # 가비지 컬렉션 방지
        else:
            print("먼저 이미지를 열어야 합니다.")  # 이미지가 없을 경우 메시지 표시

    def save_image():
        # 원본 크기의 외곽선 이미지를 저장
        if contour_image_full is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if file_path:
                contour_image_full.save(file_path)  # 원본 크기의 이미지 저장
                print(f"저장 완료: {file_path}")
        else:
            print("먼저 외곽선 추출 기능을 수행해야 합니다.")

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
