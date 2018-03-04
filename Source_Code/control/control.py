
import sys
import pandas as pd
import cv2
import numpy as np

from ..config import Config
from Source_Code import Image
from .control_funcs import subtract_func, color_segment_func, analyze_mask_func

import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt

class Control:

    def __init__(self, file_list, basepath, func_list, rock_type, *args, **kwargs):
        self.dataframe = pd.DataFrame(columns = ['image_group','before_image','after_image','output_image'])
        self.func_list = func_list
        self.rock_type = rock_type

        # Loads a list of images and their associated pairs
        for file in file_list:
            image_string = file[:11]
            if file[12:14] == 'af':
                before_image = image_string + "_abraded.jpg"
                self.add_image_pair(before_image, file, basepath)

    @classmethod
    def from_config(cls, config):
        file_list = config.get_file_paths()
        basepath = config.get_basepath()
        func_list = config.get_run_list()
        rock_type = config.get_rock_type()
        return cls(file_list, basepath, func_list, rock_type)

    def add_image_pair(self, before_image, after_image, basepath, *args, **kwargs):
        new_pair = pd.DataFrame(data = {'image_group': before_image,
                                            'before_image': [Image(basepath, before_image, *args, **kwargs)],
                                            'after_image':  [Image(basepath, after_image, *args, **kwargs)],
                                            'output_image': [None]})
        self.dataframe = pd.concat([self.dataframe, new_pair], ignore_index=True)

    def apply_func(self, func, *args, **kwargs):
        func_dict = {"subtract": subtract_func,
                     "color_segment": color_segment_func,
                     "analyze_mask_block": analyze_mask_func}

        self.dataframe.apply(func_dict[func], *args, axis = 1, **kwargs)

    def run(self):
        for func in self.func_list:
            if func == "color_segment":
                self.apply_func(func, rock_type = self.rock_type)
            else:
                self.apply_func(func)

        for i, image in enumerate(self.dataframe["after_image"]):
            plt.subplot(2, 2, i+1), plt.imshow(image["analyzed_image"], cmap = "RdYlGn")
        plt.show()
