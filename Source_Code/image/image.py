import cv2
from utils import utils

class Image:

    def __init__(self, basepath, image, readType = 0):
        self.image_data = {}
        self.image_name = image
        self.image_data['orig_image_data'] = cv2.imread(basepath + image, readType)

    def __getitem__(self, index):
        return self.image_data[index]

    def normalize_image(self, newMin = 0, newMax = 1):
        self.image_data['norm_image_data'] = utils.normalize(self.image_data['orig_image_data'], 0, 1)

    def xy_extent(self):
        return (len(self.image_data['orig_image_data']),
                len(self.image_data['orig_image_data'][0]))
