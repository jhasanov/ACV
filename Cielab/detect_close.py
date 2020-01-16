import numpy as np
import cv2
import pyautogui
import tkinter as tk
from tkinter import filedialog
from colormath.color_diff_matrix import delta_e_cie2000
import sys
sys.setrecursionlimit(6000)


width, height = pyautogui.size()
scale = 0.5
size = int(width*scale), int(height*scale)
m_loc = None
x0, y0 = (0, 0)
slctd_vec = np.array(3)
thresh = 30
image = None
copy = None
binary_map = None


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


def display_image(imag, to_select=False):
    cv2.imshow("image", imag)
    cv2.namedWindow('image')
    if to_select:
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
    print(dist)
    if dist < thresh:
        return True
    return False


def explore(x, y, dir=4):
    global image, binary_map, m_loc, size, cnt
    x0, y0 = m_loc
    # print(x, y)
    print(x, y, x0, y0, size[0], size[1], cnt)
    cnt += 1
    # print(image.shape)

    # if binary_map[x, y] < 0:
    if x >= size[1] or y >= size[0] or x <= 0 or y <= 0:
        return 0
    print(binary_map[x, y])
    if binary_map[x, y] >= 0:
        return 0
    # if True:
    if not is_close(x0, y0, x, y):
        binary_map[x, y] = 0
        return 0
    else:
        binary_map[x, y] = 1
        # copy[x, y] = 255
        # print(copy[x, y])
        # try:
        if dir==4:
            explore(x+1, y, dir=0)
            explore(x, y+1, dir=1)
            explore(x, y-1, dir=2)
            explore(x-1, y, dir=3)
        if dir==0:
            explore(x+1, y, dir=0)
            explore(x, y+1, dir=1)
            explore(x, y-1, dir=2)
        if dir==1:
            explore(x, y+1, dir=1)
            explore(x+1, y, dir=0)
            explore(x-1, y, dir=3)
        if dir==2:
            explore(x, y-1, dir=2)
            explore(x-1, y, dir=3)
            explore(x+1, y, dir=0)
        if dir==3:
            explore(x-1, y, dir=3)
            explore(x, y+1, dir=1)
            explore(x, y-1, dir=2)
        # except:
        #     None

        return 0
        # else:




def paint_closes(x, y):
    global binary_map, image
    explore(x, y)
    # binary_map[binary_map == 0] = 127
    binary_map[binary_map < 0] = 0
    binary_map[binary_map == 1] = 255
    # map = binary_map[:, :, np.newaxis] + binary_map + binary_map
    # map = np.uint8(np.stack((binary_map, binary_map, binary_map), axis=2))
    map = np.uint8(binary_map)
    print(image.shape, map.shape, map.dtype, image.dtype)
    # print(map)
    img = cv2.bitwise_and(image, image, mask=map)
    cv2.imshow("original image", image)
    cv2.imshow("image", img)
    return map


if __name__ == '__main__':

    while True:
        file_path = image_path_prompt()
        image = load_lab_image(file_path)
        binary_map = np.full(image.shape[:-1], -1)
        copy = image.copy()
        cnt = 0
        display_image(image, True)
        # display_image(binary_map)
        cv2.destroyAllWindows()


