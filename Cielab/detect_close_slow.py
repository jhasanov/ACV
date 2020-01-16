import numpy as np
import cv2
import pyautogui
import tkinter as tk
from tkinter import filedialog
from colormath.color_diff_matrix import delta_e_cie2000
width, height = pyautogui.size()
scale = 0.5
size = int(width*scale), int(height*scale)
thresh = 7

def image_path_prompt():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(title='Select an Image')
    return file_path


def load_lab_image(src):
    global size
    image = cv2.imread(src)
    img_scaled = cv2.resize(image, size, interpolation=cv2.INTER_AREA)
    lab_im = cv2.cvtColor(img_scaled, cv2.COLOR_BGR2LAB)
    return lab_im


def display_image(imag):
    cv2.imshow("image", imag)
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', on_mouse)
    # finish selecting with any key
    cv2.waitKey(0)

def on_mouse(event, x, y, flags, p2):
    global m_loc
    if event == cv2.EVENT_LBUTTONDBLCLK:
        m_loc = (y, x)
        # explore(y, x)
        paint_closes(y, x)


def is_close(x0, y0, x1, y1):
    global thresh, image
    color_vec = np.array(image[x0, y0, :])
    color_mat = np.array([(image[x1, y1, 0], image[x1, y1, 1], image[x1, y1, 2])])
    dist = np.asscalar(delta_e_cie2000(color_vec, color_mat)[0])
    # print(dist)
    if dist < thresh:
        print(dist)
        return True
    return False

def paint_closes(x, y):
    global binary_map, image
    binary_map = np.full(image.shape[:-1], 0)
    try:
        explore_side(x, y, 0)
        explore_side(x, y, 1)
        explore_side(x, y, 2)
        explore_side(x, y, 3)
    except:
        None
    mask = np.uint8(binary_map)
    print(image.shape, mask.shape, mask.dtype, image.dtype)
    # print(map)
    img = cv2.bitwise_and(image, image, mask=mask)
    cv2.imshow("image", img)



def explore_side(x, y, orientation):
    if binary_map[x, y] == -1:
        if orientation == 0:
            if is_close(x, y, x - 1, y + 1):
                binary_map[x - 1, y + 1] = 1
                explore_side(x - 1, y + 1, orientation)
            if is_close(x, y, x, y + 1):
                binary_map[x, y + 1] = 1
                explore_side(x, y + 1, orientation)
            if is_close(x, y, x + 1, y + 1):
                binary_map[x + 1, y + 1] = 1
                explore_side(x + 1, y + 1, orientation)
            print('side {} done'.format(orientation))
            return 0
        if orientation == 1:
            if is_close(x, y, x + 1, y - 1):
                binary_map[x + 1, y - 1] = 1
                explore_side(x + 1, y - 1, orientation)
            if is_close(x, y, x + 1, y):
                binary_map[x + 1, y] = 1
                explore_side(x + 1, y, orientation)
            if is_close(x, y, x + 1, y + 1):
                binary_map[x + 1, y + 1] = 1
                explore_side(x + 1, y + 1, orientation)
            print('side {} done'.format(orientation))
            return 0
        if orientation == 2:
            if is_close(x, y, x - 1, y - 1):
                binary_map[x - 1, y - 1] = 1
                explore_side(x - 1, y - 1, orientation)
            if is_close(x, y, x, y - 1):
                binary_map[x, y - 1] = 1
                explore_side(x, y - 1, orientation)
            if is_close(x, y, x + 1, y - 1):
                binary_map[x + 1, y - 1] = 1
                explore_side(x + 1, y - 1, orientation)
            print('side {} done'.format(orientation))
            return 0
        if orientation == 3:
            if is_close(x, y, x - 1, y - 1):
                binary_map[x - 1, y - 1] = 1
                explore_side(x - 1, y - 1, orientation)
            if is_close(x, y, x - 1, y):
                binary_map[x - 1, y] = 1
                explore_side(x - 1, y, orientation)
            if is_close(x, y, x - 1, y + 1):
                binary_map[x - 1, y + 1] = 1
                explore_side(x - 1, y + 1, orientation)
            print('side {} done'.format(orientation))
            return 0


if __name__ == '__main__':
    file_path = image_path_prompt()
    image = load_lab_image(file_path)
    # binary_map = np.full(image.shape[:-1], -1)
    # copy = image.copy()
    display_image(image)
    # display_image(binary_map)
    cv2.destroyAllWindows()