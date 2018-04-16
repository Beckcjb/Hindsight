import sys
import numpy as np
import cv2

# Basic normalization function
def normalize(image, newMin, newMax):
    image = ((image - image.min()) * ((newMax - newMin) / (image.max() - image.min()))) + newMin
    return image

def map_dust_colors(rock_type):
    colors = {"RockA": [],
              "RockB": [],
              "RockC": [],
              "RockD": [],
              "RockE": [([137, 125, 135], [255, 131, 139])]}
    return colors[rock_type]

def sector_mask(shape, center, radius, angle_range):
    """
    Return a boolean mask for a circular sector. The start/stop angles in
    `angle_range` should be given in clockwise order.
    """

    x,y = np.ogrid[:shape[0],:shape[1]]
    cx,cy = center
    tmin,tmax = np.deg2rad(angle_range)

    # ensure stop angle > start angle
    if tmax < tmin:
            tmax += 2 * np.pi

    # convert cartesian --> polar coordinates
    r2 = (x - cx) * (x - cx) + (y - cy) * (y - cy)
    theta = np.arctan2(x - cx, y - cy) - tmin

    # wrap angles between 0 and 2*pi
    theta %= (2 * np.pi)

    # circular mask
    circmask = r2 <= radius * radius

    # angular mask
    anglemask = theta <= (tmax - tmin)

    return circmask*anglemask

def get_percentages(mask):
    mean_array = mask.compressed()
    
    maximum = mask.max()
    minimum = mask.min()

    mean_range = maximum - minimum

    green = minimum  + mean_range * .7
    yellow = minimum  + mean_range * .3
    red = minimum

    total = len(mean_array)
    number_of_green = 0
    number_of_yellow = 0
    number_of_red = 0

    for mean in mean_array:
        if mean > green:
            number_of_green += 1
        elif mean > yellow:
            number_of_yellow += 1
        else:
            number_of_red += 1

    return [(number_of_green/total)*100, (number_of_yellow/total)*100, (number_of_red/total)*100]
