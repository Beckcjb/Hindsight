import cv2
import numpy as np
import pandas as pd
from utils.utils import map_dust_colors

def normalize_func(row, newMin = 0, newMax = 1):
    row['before_image'].normalize_image(newMin = newMin, newMax = newMax)
    row['after_image'].normalize_image(newMin = newMin, newMax = newMax)

# Func needs work but the concept is there
def subtract_func(row, data = 'orig_image_data', varThresh = .055, varInit = .3,
                                                 varMin = 0, varMax = 1, useNorm = True):
    if useNorm:
        try:
            img1 = row['before_image']['norm_image_data']
            img2 = row['after_image']['norm_image_data']
        except KeyError:
            raise KeyError('Images do not have their associated normalized images.')
    else:
        img1 = row['before_image'][data]
        img2 = row['after_image'][data]

    fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows = False)
    fgbg.setVarThreshold(varThresh)
    fgbg.setVarInit(varInit)
    fgbg.setVarMax(varMax)
    fgbg.setVarMin(varMin)
    fgbg.apply(img2)
    img_mask = fgbg.apply(img1)
    row['before_image'].sub_mask = img_mask
    row['after_image'].sub_mask = img_mask

def convert_func(row, from_image, to_image, conversion_type):
    row['before_image'].convert(from_image, to_image, conversion_type)
    row['after_image'].convert(from_image, to_image, conversion_type)

def analyze_mask(row, mask, buffer = 10, step = 1):
    image = row['after_image']
    masks = {'color_mask': image.color_mask}

    try:
        mask = masks[mask]
    except:
        raise KeyError('The mask' + mask + 'does not exist.')

    means = []
    for i in range(0, image.xy_extent()[0], step):
        for j in range(0, image.xy_extent()[1], step):
            crop = mask[i:(i + buffer), j:(j + buffer)]
            means.append(np.mean(crop))

    point_values = (means / max(means)) * 100
    # mask_df = pd.DataFrame(data = {"x_coord": x_coords,
    #                                "y_coord": y_coords,
    #                                "mean": means,
    #                                "point_value": point_values})
    image.test = point_values

def color_segment(row, rock_type):
    boundaries = map_dust_colors(rock_type)

    image = row['after_image']

    for (lower, upper) in boundaries:
        lower = np.array(lower, dtype = "uint8")
        upper = np.array(upper, dtype = "uint8")
        mask = cv2.inRange(image['lab_image_data'], lower, upper)

    image.color_mask = np.invert(mask)
