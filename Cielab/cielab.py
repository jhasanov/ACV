# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 10:21:04 2019

@author: Aydin
"""

from tkinter import *
from tkinter.filedialog import askopenfilename

# this array will have the mouse selected coordinates of the image that we will crop
arr=[]

#following code block allows to selec a picture from a folder, then stores the mouse clicks in the array.
#we are not limited to a rectangular shape, indeed we can crop any polygonal shape 
#the mouse selection of the coordinates MUST be Clockwise, close the picture once you are done with selecting points.


#CODE BLOCK 1
event2canvas = lambda e, c: (c.canvasx(e.x), c.canvasy(e.y))

root = Tk()

#setting up a tkinter canvas with scrollbars
frame = Frame(root, bd=2, relief=SUNKEN)
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)
xscroll = Scrollbar(frame, orient=HORIZONTAL)
xscroll.grid(row=1, column=0, sticky=E+W)
yscroll = Scrollbar(frame)
yscroll.grid(row=0, column=1, sticky=N+S)
canvas = Canvas(frame, bd=0, xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
canvas.grid(row=0, column=0, sticky=N+S+E+W)
xscroll.config(command=canvas.xview)
yscroll.config(command=canvas.yview)
frame.pack(fill=BOTH,expand=1)

#adding the image
File = askopenfilename(parent=root, initialdir="M:/",title='Choose an image.')
print("opening %s" % File)
img = PhotoImage(file=File)
canvas.create_image(0,0,image=img,anchor="nw")
canvas.config(scrollregion=canvas.bbox(ALL)) 

#function to be called when mouse is clicked   
def printcoords(event):
    #outputting x and y coords to console
    cx, cy = event2canvas(event, canvas)
    print ("(%d, %d)" % (cx,cy))
    arr.append((event.x,event.y));
#mouseclick even
for i in range(0,4):
    canvas.bind("<ButtonPress-1>",printcoords)


root.mainloop()

#END OF CODE BLOCK 1


#Following code block crops the image in polygonal form, using the mouse selected coordinates. 

#CODE BLOCK 2
import numpy
from PIL import Image, ImageDraw

# read image as RGB and add alpha (transparency)
im = Image.open("cat.png").convert("RGBA")

# convert to numpy (for convenience)
imArray = numpy.asarray(im)


maskIm = Image.new('L', (imArray.shape[1], imArray.shape[0]), 0)
ImageDraw.Draw(maskIm).polygon(arr, outline=1, fill=1)
mask = numpy.array(maskIm)

# assemble new image (uint8: 0-255)
newImArray = numpy.empty(imArray.shape,dtype='uint8')

# colors (three first columns, RGB)
newImArray[:,:,:3] = imArray[:,:,:3]

# transparency (4th column)
newImArray[:,:,3] = mask*255

# back to Image from numpy
newIm = Image.fromarray(newImArray, "RGBA")

#our selected piece of the image now saved.
newIm.save("polygonalCrop.png")


#END OF CODE BLOCK 2

#Following code first converts our selected piece to L*a*b makes 
# by making conversions to meet requirements of the rgb2lab()
from skimage import io, color
#rgb = values of the original image
#rgb = values of the cropped image
rgb = Image.open("polygonalCrop.png").convert("RGB")
rgbArray=numpy.asarray(rgb);
#lab values of the cropped image
lab = color.rgb2lab(rgbArray)

