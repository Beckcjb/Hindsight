import sys
import cv2
import os
import math
import numpy as np
from ..utils import utils

class Image:

    def __init__(self, basepath, image, readType = 1):
        self.image_data = {}
        self.image_name = image
        self.image_path = os.path.join(basepath, image)
        self.image_data['orig_image_data'] = cv2.imread(self.image_path, readType)

    def __getitem__(self, index):
        return self.image_data[index]

    def normalize_image(self, newMin = 0, newMax = 1):
        self.image_data['norm_image_data'] = utils.normalize(self.image_data['orig_image_data'], newMin, newMax)

    def xy_extent(self):
        return (len(self.image_data['orig_image_data']),
                len(self.image_data['orig_image_data'][0]))

    def convert(self, from_image, to_image, conversion_type):
         self.image_data[to_image] = cv2.cvtColor(self.image_data[from_image], conversion_type)

    def subtract(self, sub_image, data, varThresh = .055, varInit = .3,
                                        varMin = 0, varMax = 1, useNorm = True):
        if useNorm:
            try:
                img1 = self['norm_image_data']
                img2 = sub_image['norm_image_data']
            except KeyError:
                self.image_data['norm_image_data'] = utils.normalize(self.image_data['orig_image_data'], 0, 1)
                sub_image.image_data['norm_image_data'] = utils.normalize(self.image_data['orig_image_data'], 0, 1)

                img1 = self['norm_image_data']
                img2 = sub_image['norm_image_data']
        else:
            img1 = self[data]
            img2 = sub_image[data]

        fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows = False)
        fgbg.setVarThreshold(varThresh)
        fgbg.setVarInit(varInit)
        fgbg.setVarMax(varMax)
        fgbg.setVarMin(varMin)
        fgbg.apply(img2)
        img_mask = fgbg.apply(img1)
        self.image_data['sub_mask'] = img_mask
        sub_image.image_data['sub_mask']  = img_mask

    def extract_circle(self, center, radius):
        circular_mask = utils.sector_mask(self.shape, center = center,
                                          radius = radius, angle_range = (0, 360));
        return 0

    def analyze_mask_block(self, mask, buffer = 10, center = (1150, 1100), radius = 375):
        line = []
        analyzed_image = []
        x, y = self.xy_extent()

        for i in range(0, x, buffer):
            for j in range(0, y, buffer):
                crop = mask[i:(i + buffer), j:(j + buffer)]
                mean = np.mean(crop)
                area = np.full((buffer, buffer), mean)
                if len(line) == 0:
                     line = area
                else:
                    line = np.concatenate((line, area), axis = 1)
            if len(analyzed_image) == 0:
                analyzed_image = line
            else:
                analyzed_image= np.concatenate((analyzed_image, line), axis = 0)
            line = []

        circular_mask = utils.sector_mask(analyzed_image.shape, center, radius, (0, 360))
        analyzed_image = np.ma.array(analyzed_image, mask=np.invert(circular_mask))

        self.image_data['analyzed_image'] = analyzed_image
        self.image_data['percentages'] = utils.get_percentages(analyzed_image)

    def analyze_mask_circlular(self, mask, buffer = 10, center = (1150, 1100), radius = 375, band_size = .7):
        orig_radius = radius
        avg_pixel_val = (np.min(mask) + np.max(mask))/2
        analyzed_image = np.full(mask.shape, avg_pixel_val)

        while(radius > 10):
            circular_mask = utils.sector_mask(mask.shape, center, radius, (0, 360))
            new_mask = np.ma.array(mask, mask=np.invert(circular_mask))

            compressed_image = new_mask.compressed()
            mean = sum(compressed_image)/len(compressed_image)

            for i in range(0, len(mask), buffer):
                for j in range(0, len(mask[i]), buffer):
                    if new_mask[i][j]:
                        analyzed_image[i:i+buffer, j:j+buffer] = mean

            radius = radius * band_size

        circular_mask = utils.sector_mask(analyzed_image.shape, center, orig_radius, (0, 360))
        analyzed_image = np.ma.array(analyzed_image, mask=np.invert(circular_mask))

        self.image_data['analyzed_image'] = analyzed_image
        self.image_data['percentages'] = utils.get_percentages(analyzed_image)

    def color_segment(self, rock_type):
        self.convert("orig_image_data", "lab_image_data", cv2.COLOR_BGR2LAB)
        boundaries = utils.map_dust_colors(rock_type)

        for (lower, upper) in boundaries:
            lower = np.array(lower, dtype = "uint8")
            upper = np.array(upper, dtype = "uint8")
            mask = cv2.inRange(self['lab_image_data'], lower, upper)

        self.image_data['color_mask'] = np.invert(mask)

    def ml_color_segment(self, image, rock_type, eng):
        if rock_type == 'RockE':
            mask, _ = eng.rockEMatlabColorSegment(image, nargout=2)
        else:
            raise KeyError('No color segmentation for rock type: {}'.format(rock_type))

        np_mask = np.array(mask._data.tolist())
        (x, y) = mask.size[1], mask.size[0]
        np_mask = np.invert(np_mask.reshape((x, y)).transpose())
        self.image_data['color_mask'] = np_mask
