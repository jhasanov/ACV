import numpy as np
import cv2
import sys
import pyautogui
import tkinter as tk
from tkinter import filedialog
from Cielab.rect_area import get_image_stats
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
width, height = pyautogui.size()
scale = 0.5
size = int(width*scale), int(height*scale)

def load_image(src):
    global size
    image = cv2.imread(src)
    img_scaled = cv2.resize(image, size, interpolation=cv2.INTER_AREA)
    # lab_im = cv2.cvtColor(img_scaled, cv2.COLOR_BGR2LAB)
    return img_scaled

def convert_image(image):
    lab_im = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    bgr_im = cv2.cvtColor(lab_im, cv2.COLOR_LAB2BGR)
    return bgr_im


def compare_2_images(image1, image2):
    std1 = list()
    std2 = list()
    mean1 = list()
    mean2 = list()
    squared_error = list()
    for channel in range(image1.shape[2]):
        im1_channel_data = np.array(image1[:, :, channel]).flatten()
        im2_channel_data = np.array(image2[:, :, channel]).flatten()
        std1.append(np.std(im1_channel_data, dtype=np.float64))
        std2.append(np.std(im2_channel_data, dtype=np.float64))
        mean1.append(np.mean(im1_channel_data, dtype=np.float64))
        mean2.append(np.mean(im2_channel_data, dtype=np.float64))

        sq_err = ((im1_channel_data - im2_channel_data)**2).mean()
        squared_error.append(sq_err)

    # print(squared_error)
    return mean1, std1, mean2, std2, squared_error


if __name__ == '__main__':
    while True:
        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename(title='Select an Image')
        # print(type(file_path), file_path)
        try:
            image = load_image(file_path)
        except:
            break
        converted_image = convert_image(image)
        print(compare_2_images(image, converted_image))
        for i in range(10):
            converted_image = convert_image(converted_image)
            mean1, std1, mean2, std2, squared_error = compare_2_images(image, converted_image)
            mean_diff = np.subtract(mean1, mean2)
            std_diff = np.subtract(std1, std2)
            print('Iteration : {}\n'.format(i),
                  'mean1_B: {0} - mean2_B: {1} = {2}\n'.format(mean1[0], mean2[0], mean_diff[0]),
                  'mean1_G: {0} - mean2_G: {1} = {2}\n'.format(mean1[1], mean2[1], mean_diff[1]),
                  'mean1_R: {0} - mean2_R: {1} = {2}\n'.format(mean1[2], mean2[2], mean_diff[2]),
                  'std1_B: {0} - std2_B: {1} = {2}\n'.format(std1[0], std2[0], std_diff[0]),
                  'std1_G: {0} - std2_G: {1} = {2}\n'.format(std1[1], std2[1], std_diff[1]),
                  'std1_B: {0} - std2_R: {1} = {2}\n'.format(std1[2], std2[2], std_diff[2]))
        difference = cv2.subtract(image, converted_image)
        squared_error = ((image - converted_image)**2)
        # print(image)
        images = list()
        a = np.multiply(image, squared_error)
        # multiplied = np.nan_to_num(np.divide(a, squared_error))
        multiplied = np.array(a)
        # print(multiplied)
        images.append(multiplied)
        # get_image_stats(images, pdf_path=file_path[:-4]+'.pdf', chnl_list=['Blue', 'Green', 'Red'])
        # print(difference)
        # difference[difference == 0] = 255
        # difference = 255 - difference
        # print(difference)
        print(compare_2_images(image, converted_image))

        cv2.imshow("image", multiplied)
        cv2.waitKey(0)