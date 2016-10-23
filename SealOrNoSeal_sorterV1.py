#!/bin/python
# SealorNoSeal seal sorter v1. 


import glob
import skimage as sk
import numpy as np
import time

from skimage.exposure import rescale_intensity
from skimage import data
from skimage.color import rgb2hed
from skimage.color import rgb2hsv
from skimage.color import rgb2lab



ImagePath = "/home/mike/Dropbox/Mike/GIT/SealOrNoSeal/TestImages"
Reference = "fake_no_sealtest.jpg"
ImageExtention = "*.JPG"


def background_image(img):
    """ A function to take a reference image and create a background mask to 
    subtract from image processing"""
    image = sk.io.imread(img)
    # convert colorspace:
    img_hsv = rgb2hsv(image)
    img_hed = rgb2hed(image)
    img_lab = rgb2lab(image)

    s1 = rescale_intensity(img_hsv[:, :, 1], out_range=(0, 1))
    s2 = rescale_intensity(img_hed[:, :, 1], out_range=(0, 1))
    s4 = rescale_intensity(img_lab[:, :, 1], out_range=(0, 1))

    img_raw = (s1 * s2 * s4)

    return img_raw



def seal_sorter(img, bg_img):
    """A function that does image processing on a file to determine 
    whether it is likely to contain a seal image."""
    image = sk.io.imread(img)
    # convert colorspace:
    img_hsv = rgb2hsv(image)
    img_hed = rgb2hed(image)
    img_lab = rgb2lab(image)

    s1 = rescale_intensity(img_hsv[:, :, 1], out_range=(0, 1))
    s2 = rescale_intensity(img_hed[:, :, 1], out_range=(0, 1))
    s4 = rescale_intensity(img_lab[:, :, 1], out_range=(0, 1))
 
    img_raw = (s1 * s2 * s4)
    img_p = img_raw - bg_img
    score = np.sum(img_p > 0.05) / img_p.size

    return score


if __name__ == "__main__":

# sort through image list:
    target = ImagePath + "/" + ImageExtention
    filelist = glob.glob(target)
# initialize background image:
    bg_img = background_image(Reference)

    NoSeal   =[]
    LowSeal  =[]
    HighSeal =[]
    starttime = int(time.time())  

    n = 0 
    for i in filelist:   
        score = seal_sorter(i, bg_img)
        n += 1
        timenow = int(time.time()-starttime)
        print(" {} {} Image: {} Score: {}".format(n,timenow,i[-16:],score))
 





