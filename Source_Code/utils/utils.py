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
