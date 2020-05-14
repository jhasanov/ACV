import numpy as np
import cv2
import tkinter as tk
from tkinter import filedialog
import itertools
import pyautogui
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import colour
# src = 'let_there_be_colour.png'
# size = (1280, 960)
# bounds = dict()
# bounderies = list()
# captures = list()


def ask_image_path():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title='Select an Image')
    return file_path


def get_size(scale=0.3):
    width, height = pyautogui.size()
    size = int(width*scale), int(height*scale)
    return size


def load_image(src):
    size = get_size()
    image = cv2.imread(src)
    img_scaled = cv2.resize(image, size, interpolation=cv2.INTER_AREA)
    # lab_im = cv2.cvtColor(img_scaled, cv2.COLOR_BGR2LAB)
    return img_scaled


def BGR2LAB(image):
    """
    Converts OpenCV BGR image to CIE Lab image
    Lab   Scale
    L|    0:100 |
    a| -100:100 |
    b| -100:100 |

    :param image: BGR image
    :return: Lab image
    """
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_srgb = image_rgb.astype(np.float32) / 255
    image_lab = colour.XYZ_to_Lab(colour.sRGB_to_XYZ(image_srgb))

    return image_lab


def LAB2RGB(image):
    """
    Convert image from CIE Lab to RGB colour space
    Lab   Scale
    L|    0:100 |
    a| -100:100 |
    b| -100:100 |

    :param image:
    :return:
    """
    image_sRGB = colour.XYZ_to_sRGB(colour.Lab_to_XYZ(image))
    image_RGB = np.round(image_sRGB*255).astype(np.uint8)
    return image_RGB

def delta_E_range():
    XYZ = colour.volume.XYZ_outer_surface()
    # print(XYZ, XYZ.shape)
    combinations = colour.XYZ_to_Lab(np.array(list(itertools.combinations(XYZ, 2))))
    # print(combinations)
    delta_E = colour.delta_E(combinations[:, 0, :], combinations[:, 1, :])
    return np.amax(delta_E), np.amin(delta_E)


if __name__ == '__main__':
    # image = load_image()
    # img = image.copy()
    # display_image(img)
    # get_image_stats(captures)
    # cv2.destroyAllWindows()

    image = load_image(ask_image_path())
    image_lab = BGR2LAB(image)
    image_rgb = LAB2RGB(image_lab)
    plt.imshow(image_rgb)
    plt.show()
    print(image_lab,
          np.amax(image_lab[:,:, 0]),
          np.amax(image_lab[:,:, 1]),
          np.amax(image_lab[:,:, 2]),
          np.amin(image_lab[:,:, 0]),
          np.amin(image_lab[:,:, 1]),
          np.amin(image_lab[:,:, 2]))

    # print(delta_E_range())


