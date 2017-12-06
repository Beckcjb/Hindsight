import numpy as np
import cv2

# Basic normalization function
def normalize(image, newMin, newMax):
    image = ((image - image.min()) * ((newMax - newMin)/(image.max() - image.min()))) + newMin
    return image

def normalize_func(row, newMin = 0, newMax = 1):
    row['before_image'].normalize_image(newMin = newMin, newMax = newMax)
    row['after_image'].normalize_image(newMin = newMin, newMax = newMax)

# Func needs work but th concept is there
def subtract_func(row, varThresh = .055, varInit = .3, varMix = 0, varMax = 1, useNorm = True):
    if useNorm:
        try:
            img1 = row['before_image']['norm_image_data']
            img2 = row['after_image']['norm_image_data']
        except KeyError:
            raise KeyError('Images do not have their associated normalized images.')
    else:
        img1 = row['before_image']['orig_image_data']
        img2 = row['after_image']['orig_image_data']

    fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows = False)
    fgbg.setVarThreshold(.055)
    fgbg.setVarInit(.3)
    fgbg.setVarMax(1)
    fgbg.setVarMin(0)
    fgbg.apply(img2)
    img_mask = fgbg.apply(img1)
    row['before_image'].sub_mask = img_mask
    row['after_image'].sub_mask = img_mask
