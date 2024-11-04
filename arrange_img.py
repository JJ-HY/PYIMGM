import tkinter as tk
from tkinter import filedialog, Toplevel, messagebox
from PIL import Image, ImageTk

def open_multiple_images(root):
    new_window = Toplevel(root)
    new_window.title("PYIMGM")
    new_window.geometry("500x600")

    title_label = tk.Label(new_window, text="이미지 크기 변경", font=("bold", 12))
    title_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)

    # new_window grid
    new_window.grid_rowconfigure(0, weight=0)  # title
    new_window.grid_rowconfigure(1, weight=1)  # image
    new_window.grid_rowconfigure(2, weight=0)  # button
    new_window.grid_columnconfigure(0, weight=1)  # button

    img_display = tk.Label(new_window)
    img_display.grid(row=1, column=0, padx=20, pady=20)

    image_paths = []
    image_listbox = tk.Listbox(new_window, width=50, height=10)
    image_listbox.grid(row=2, column=0, padx=20, pady=10)

    def load_images():
        file_paths = filedialog.askopenfilenames(parent=new_window, filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_paths:
            for file_path in file_paths:
                image_paths.append(file_path)
                image_listbox.insert(tk.END, file_path.split("/")[-1])

    def resize_images():
        if not image_paths:
            messagebox.showwarning("경고", "이미지를 먼저 불러와야 합니다.")
            return

        try:
            target_width = int(size_entry.get())  # get width size
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

        try:
            target_width = int(size_entry.get())  # 사용자가 입력한 가로 크기
        except ValueError:
            messagebox.showerror("오류", "유효한 숫자를 입력하세요.")
            return

        # Load and resize images to the specified width
        images = [Image.open(path).resize((target_width, int(target_width * (Image.open(path).height / Image.open(path).width))), Image.LANCZOS) for path in image_paths]
        total_height = sum(img.height for img in images) + 5 * (len(images) - 1)  # 이미지 높이 총합 + 간격 합

        # Create new image with white background
        concatenated_img = Image.new("RGB", (target_width, total_height), (255, 255, 255))

        # Paste images vertically
        y_offset = 0
        for img in images:
            concatenated_img.paste(img, (0, y_offset))  # 이미지 붙이기
            y_offset += img.height + 5  # 현재 이미지 높이 + 간격을 더해 다음 위치 계산

        # Save concatenated image
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")],
                                                 initialfile="concatenated_image.png")
        if save_path:
            concatenated_img.save(save_path)
            print(f"합성 이미지 저장 완료: {save_path}")

    open_button = tk.Button(new_window, text="이미지 열기", command=load_images)
    open_button.grid(row=0, column=0, pady=10)

    # width input 
    size_entry = tk.Entry(new_window)
    size_entry.grid(row=3, column=0, padx=10, pady=10)
    size_entry.insert(0, "가로 크기 입력")

    # frame
    button_frame = tk.Frame(new_window)
    button_frame.grid(row=4, column=0, pady=20)

    # resize_button
    resize_button = tk.Button(button_frame, text="사이즈 변경", command=resize_images)
    resize_button.pack(side="left", padx=10)

    # concatenate_images
    open_images_button = tk.Button(button_frame, text="여러 이미지 합성", command=concatenate_images)
    open_images_button.pack(side="left", padx=10)

    # save
    save_button = tk.Button(button_frame, text="이미지 저장", command=resize_images)
    save_button.pack(side="left", padx=10)
