import numpy as np
import cv2
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

src = 'let_there_be_colour.png'
bounds = dict()
bounderies = list()
captures = list()


def load_image(src=src):
    image = cv2.imread(src)
    lab_im = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    return lab_im


def display_image(image):
    # todo: scale the image
    cv2.imshow("image", image)
    # cv2.namedWindow('image')
    cv2.setMouseCallback('image', on_mouse)
    cv2.waitKey(0)
    select(image)


def on_mouse(event, x, y, flags, p2):
    global bounds, bounderies
    if event == cv2.EVENT_LBUTTONDOWN and len(bounds) < 1:
        x1, y1 = x, y
        bounds['x1'] = x1
        bounds['y1'] = y1
    if event == cv2.EVENT_LBUTTONUP and len(bounds) < 3:
        x2, y2 = x, y
        bounds['x2'] = x2
        bounds['y2'] = y2
    if event == cv2.EVENT_RBUTTONDBLCLK:
        bounderies.append(bounds)
        bounds = dict()
        print('ctrl')


def select(image):
    global captures, bounderies
    for boundery in bounderies:
        x1 = boundery['x1']
        x2 = boundery['x2']
        y1 = boundery['y1']
        y2 = boundery['y2']
        # todo: show selection box
        roi = image[y1:y2, x1:x2]
        captures.append(roi)
        cv2.imwrite('captured_' + str(len(captures)) + '.png', roi)


def get_image_stats(im_list):
    name = str(src[:-4] + '.pdf')
    pp = PdfPages(name)
    for idx in range(3):
        channel = list()
        for imag in im_list:
            chnl = list(np.array(imag[:, :, idx]).flatten())
            channel.extend(chnl)
        get_stats(channel, pp, str('Channel: ' + str(idx) + ' histogram'))
    pp.close()


def get_stats(values, pp, title):
    std = np.std(values, dtype=np.float64)
    mean = np.mean(values, dtype=np.float64)
    plt.figure()
    # todo: determine number of bins
    # todo: display more informative data
    plt.hist(values, bins='auto')
    plt.title(title + '\nstd: ' + str(std) + '\nmean: ' + str(mean))
    pp.savefig()


display_image(load_image())
get_image_stats(captures)

