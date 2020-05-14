# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 10:21:04 2019

@author: Aydin
"""

from skimage import io, color
rgb = io.imread('cat.png')
lab = color.rgb2lab(rgb)
from PIL import Image
im = Image.open(r"cat.png")
  
# Size of the image in pixels (size of orginal image) 
# (This is not mandatory) 
width, height = im.size 
  
# Setting the points for cropped image 

  
# Cropped image of above dimension 
# (It will not change orginal image) 
cropped = im.crop((330, 300, 420, 420)) 

# Shows the image in image viewer 
cropped.show() 

cropped.save('dat.png')

croppedLab_rgb=io.imread(cropped)