import tkinter as tk
from tkinter import filedialog, Toplevel, messagebox
from PIL import Image, ImageTk

def open_multiple_images(root):
    new_window = Toplevel(root)
    new_window.title("PYIMGM")
    new_window.geometry("500x600")

    title_label = tk.Label(new_window, text="이미지 크기 변경", font=("bold", 12))
    title_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)

    # 새 창의 레이아웃을 설정 (grid 사용)
    new_window.grid_rowconfigure(0, weight=0)  # 제목
    new_window.grid_rowconfigure(1, weight=1)  # 이미지가 중간에 위치
    new_window.grid_rowconfigure(2, weight=0)  # 버튼이 하단에 위치
    new_window.grid_columnconfigure(0, weight=1)  # 버튼과 이미지 중앙 정렬

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

    def concatenate_images():
        if not image_paths:
            messagebox.showwarning("경고", "이미지를 먼저 불러와야 합니다.")
            return

        images = [Image.open(path) for path in image_paths]
        total_height = sum(img.height for img in images) + 5 * (len(images) - 1)  # 이미지 높이 총합 + 간격 합
        max_width = max(img.width for img in images)  # 가장 넓은 이미지의 가로 크기

        # 합성 이미지 생성 (배경색을 흰색으로 설정)
        concatenated_img = Image.new("RGB", (max_width, total_height), (255, 255, 255))

        # 이미지들을 세로로 붙이기
        y_offset = 0
        for img in images:
            concatenated_img.paste(img, (0, y_offset))  # 이미지 붙이기
            y_offset += img.height + 5  # 현재 이미지 높이 + 간격을 더해 다음 위치 계산

        # 합성된 이미지 저장
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")],
                                                 initialfile="concatenated_image.png")
        if save_path:
            concatenated_img.save(save_path)
            print(f"합성 이미지 저장 완료: {save_path}")

    # 이미지 열기 버튼
    open_button = tk.Button(new_window, text="이미지 열기", command=load_images)
    open_button.grid(row=0, column=0, pady=10)

    # 가로 크기 입력 필드
    size_entry = tk.Entry(new_window)
    size_entry.grid(row=3, column=0, padx=10, pady=10)
    size_entry.insert(0, "가로 크기 입력")  # 기본 텍스트 설정

    # 버튼을 배치할 프레임 생성
    button_frame = tk.Frame(new_window)
    button_frame.grid(row=4, column=0, pady=20)

    # 사이즈 변경 버튼
    resize_button = tk.Button(button_frame, text="사이즈 변경", command=resize_images)
    resize_button.pack(side="left", padx=10)

    # 여러 이미지 합성 버튼 - 새로 만든 concatenate_images 함수에 연결
    open_images_button = tk.Button(button_frame, text="여러 이미지 합성", command=concatenate_images)
    open_images_button.pack(side="left", padx=10)

    # 이미지 저장 버튼
    save_button = tk.Button(button_frame, text="이미지 저장", command=resize_images)
    save_button.pack(side="left", padx=10)
