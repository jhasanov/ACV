import tkinter as tk
from PIL import Image
from PIL import ImageTk
from tkinter import filedialog
import cv2
import pyautogui

width, height = pyautogui.size()
scale = 0.3
size = int(width*scale), int(height*scale)


def image_path_prompt():
    global panelA, panelB, path

    path = filedialog.askopenfilename(title='Select an Image')
    display_lab_images(load_lab_image(path), load_lab_image(path))
    # return path


def load_lab_image(src):
    global size
    image = cv2.imread(src)
    img_scaled = cv2.resize(image, size, interpolation=cv2.INTER_AREA)
    lab_im = cv2.cvtColor(img_scaled, cv2.COLOR_BGR2LAB)
    return lab_im


def display_lab_images(image1_cv, image2_cv):
    image1_RGB = cv2.cvtColor(image1_cv, cv2.COLOR_LAB2RGB)
    image2_RGB = cv2.cvtColor(image2_cv, cv2.COLOR_LAB2RGB)
    image1_P = Image.fromarray(image1_RGB)
    image2_P = Image.fromarray(image2_RGB)
    image1 = ImageTk.PhotoImage(image1_P)
    image2 = ImageTk.PhotoImage(image2_P)
    global panelA, panelB

    if panelA is None or panelB is None:
        panelA = tk.Label(image=image1)
        panelA.image = image1
        panelA.pack(side="left", padx=10, pady=10)

        panelB = tk.Label(image=image2)
        panelB.image = image2
        panelB.pack(side="right", padx=10, pady=10)
    else:
        panelA.configure(image=image1)
        panelB.configure(image=image2)
        panelA.image = image1
        panelB.image = image2


if __name__ == '__main__':
    root = tk.Tk()
    # root.withdraw()
    panelA = None
    panelB = None
    btn = tk.Button(root, text="Select an image", command=image_path_prompt)
    btn.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")
    root.mainloop()

