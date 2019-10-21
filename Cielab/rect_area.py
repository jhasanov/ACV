import numpy as np
import cv2
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

src = 'let_there_be_colour.png'

def load_image(src=src):
    image = cv2.imread(src)
    lab_im = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    return lab_im


def select(image, x1, y1, x2, y2):
    # todo: get mouse input from user
    roi = image[y1:y2, x1:x2]
    cv2.imwrite('captured.png', roi)
    return roi


def get_image_stats(image):
    name = str(src[:-4] + '.pdf')
    pp = PdfPages(name)
    for idx in range(3):
        channel = np.array(image[:, :, idx]).flatten()
        get_stats(channel, pp, str('Channel: ' + str(idx) + ' histogram'))
    pp.close()


def get_stats(values, pp, title):
    std = np.std(values, dtype=np.float64)
    mean = np.mean(values, dtype=np.float64)
    plt.figure()
    # todo: determine number of bins
    plt.hist(values, bins='auto')
    plt.title(title + '\nstd: ' + str(std) + '\nmean: ' + str(mean))
    pp.savefig()


get_image_stats(select(load_image(), 100, 100, 400, 320))

