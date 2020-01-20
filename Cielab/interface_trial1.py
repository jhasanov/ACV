import cv2
import sys
import pyautogui
import numpy as np
from PIL import Image
from PIL import ImageTk
import tkinter as tk
from tkinter import filedialog
from colormath.color_diff_matrix import delta_e_cie2000
sys.setrecursionlimit(2000)


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.width, self.height = pyautogui.size()
        self.thresh = 20
        self.scale = 0.3
        self.size = int(self.width*self.scale), int(self.height*self.scale)
        self.panel_original = None
        self.panel_processed = None
        self.panel_auxiliary = None
        self.lab_final = None
        self.x0 = None
        self.aux_side = 64

    def create_widgets(self):
        self.select_image = tk.Button(self, text="Select an image", command=self.select_image)
        self.select_image.pack(side="top", fill="both", expand="yes", padx="10", pady="10")
        self.thresh_L = tk.Label(self, text='Threshold')
        self.thresh_L.pack(side='left')
        self.entry = tk.Entry(self)
        self.entry.pack(side='left')
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def select_image(self):
        self.__load_image()
        self.__update_image_panels()

    def __load_image(self):
        self.image_path = filedialog.askopenfilename(title='Select an Image')
        self.original_cv2 = image = cv2.imread(self.image_path)
        img_scaled = cv2.resize(image, self.size, interpolation=cv2.INTER_AREA)
        self.lab_image = cv2.cvtColor(img_scaled, cv2.COLOR_BGR2LAB)

    def __update_image_panels(self):
        if self.lab_final is None:
            self.lab_final = self.lab_image
        image1_RGB = cv2.cvtColor(self.lab_image, cv2.COLOR_LAB2RGB)
        image2_RGB = cv2.cvtColor(self.lab_final, cv2.COLOR_LAB2RGB)
        image1_P = Image.fromarray(image1_RGB)
        image2_P = Image.fromarray(image2_RGB)
        self.tk_original_image = ImageTk.PhotoImage(image1_P)
        self.tk_processed_image = ImageTk.PhotoImage(image2_P)

        if self.panel_original is None or self.panel_processed is None:
            self.panel_original = tk.Label(text='test text only', image=self.tk_original_image)
            self.panel_original.image = self.tk_original_image
            self.panel_original.pack(side="left", padx=10, pady=10)

            self.panel_processed = tk.Label(image=self.tk_processed_image)
            self.panel_processed.image = self.tk_processed_image
            self.panel_processed.pack(side="right", padx=10, pady=10)
        else:
            self.panel_original.configure(image=self.tk_original_image)
            self.panel_processed.configure(image=self.tk_processed_image)
            self.panel_original.image = self.tk_original_image
            self.panel_processed.image = self.tk_processed_image
        self.panel_original.bind("<Button-1>", self.mouse_click)
        if self.x0 is not None:
            self.fill_aux_panel()


    def mouse_click(self, event):
        self.x0 = event.y
        self.y0 = event.x
        print(self.x0, self.y0)
        if len(self.entry.get()) > 1:
            self.thresh = float(self.entry.get())
        self.paint_closes(self.x0, self.y0)

    def is_close(self, x1, y1):
        color_vec = np.array(self.lab_image[self.x0, self.y0, :])
        color_mat = np.array([(self.lab_image[x1, y1, 0], self.lab_image[x1, y1, 1], self.lab_image[x1, y1, 2])])
        dist = np.asscalar(delta_e_cie2000(color_vec, color_mat)[0])
        print(dist)
        if dist < self.thresh:
            return True
        return False

    def explore(self, x, y, dir=4):
        # global image, binary_map, m_loc, size, cnt
        # x0, y0 = m_loc
        # print(x, y)
        print(x, y, self.x0, self.y0, self.size[0], self.size[1])
        # cnt += 1
        # print(image.shape)

        # if binary_map[x, y] < 0:
        if x >= self.size[1] or y >= self.size[0] or x <= 0 or y <= 0:
            return 0
        print(self.binary_map[x, y])
        if self.binary_map[x, y] >= 0:
            return 0
        # if True:
        if not self.is_close(x, y):
            self.binary_map[x, y] = 0
            return 0
        else:
            self.binary_map[x, y] = 1
            self.coord_list.append((x+1, y))
            self.coord_list.append((x-1, y))
            self.coord_list.append((x, y+1))
            self.coord_list.append((x, y-1))
            # copy[x, y] = 255
            # print(copy[x, y])
            # try:
            # if dir==4:
            #     self.explore(x+1, y, dir=0)
            #     self.explore(x, y+1, dir=1)
            #     self.explore(x, y-1, dir=2)
            #     self.explore(x-1, y, dir=3)
            # if dir==0:
            #     self.explore(x+1, y, dir=0)
            #     self.explore(x, y+1, dir=1)
            #     self.explore(x, y-1, dir=2)
            # if dir==1:
            #     self.explore(x, y+1, dir=1)
            #     self.explore(x+1, y, dir=0)
            #     self.explore(x-1, y, dir=3)
            # if dir==2:
            #     self.explore(x, y-1, dir=2)
            #     self.explore(x-1, y, dir=3)
            #     self.explore(x+1, y, dir=0)
            # if dir==3:
            #     self.explore(x-1, y, dir=3)
            #     self.explore(x, y+1, dir=1)
            #     self.explore(x, y-1, dir=2)
            # except:
            #     None

            return 0
            # else:

    def paint_closes(self, x, y):
        # global binary_map, image
        self.binary_map = np.full(self.lab_image.shape[:-1], -1)
        self.coord_list = [(x, y)]
        while self.coord_list:
            x0, y0 = self.coord_list.pop(-1)
            self.explore(x0, y0)
        # self.explore(x, y)
        # binary_map[binary_map == 0] = 127
        self.binary_map[self.binary_map < 0] = 0
        self.binary_map[self.binary_map == 1] = 255
        # map = binary_map[:, :, np.newaxis] + binary_map + binary_map
        # map = np.uint8(np.stack((binary_map, binary_map, binary_map), axis=2))
        map = np.uint8(self.binary_map)
        print(self.lab_image.shape, map.shape, map.dtype, self.lab_image.dtype)
        # print(map)
        self.lab_final = cv2.bitwise_and(self.lab_image, self.lab_image, mask=map)
        self.__update_image_panels()
        print(self.thresh)

    def fill_aux_panel(self):
        empty_image = np.zeros((self.aux_side, self.aux_side, 3), np.uint8)
        empty_image[:] = np.array(self.lab_image[self.x0, self.y0, :])

        self.tk_auxiliary = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(empty_image, cv2.COLOR_LAB2RGB)))
        if self.panel_auxiliary is None:
            self.panel_auxiliary = tk.Label(image=self.tk_auxiliary)
            self.panel_auxiliary.image = self.tk_auxiliary
            self.panel_auxiliary.pack(side="top", padx=5, pady=5)
        else:
            self.panel_auxiliary.configure(image=self.tk_auxiliary)
            self.panel_auxiliary.image = self.tk_auxiliary

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    # app.update_image_panels()
    app.mainloop()