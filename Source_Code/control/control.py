import sys
import math

import cv2
import pandas as pd
import numpy as np
import matlab.engine

from ..config import Config
from Source_Code import Image
from .control_funcs import *

import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt

class Control:

    def __init__(self, file_list, basepath, func_list, rock_type, *args, **kwargs):
        self.dataframe = pd.DataFrame(columns = ['image_group','before_image','after_image','output_image'])
        self.func_list = func_list
        self.rock_type = rock_type
        self.matlab_engine = matlab.engine.start_matlab()
        self.matlab_engine.addpath(r'./Source_Code/color_seg_matlab')

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
                     "analyze_mask": analyze_mask_func,
                     "convert": convert_func,
                     "ml_color_segment": ml_color_segment_func}

        self.dataframe.apply(func_dict[func], *args, axis = 1, **kwargs)

    def run(self):
        for func in self.func_list:
            if func == '0':
                continue
            elif func == "color_segment":
                self.apply_func(func, rock_type = self.rock_type)
            elif func == "ml_color_segment":
                self.apply_func(func, ml_eng = self.matlab_engine)
            else:
                self.apply_func(func)

        size = math.ceil(math.sqrt(len(self.dataframe["after_image"])))
        percentage_string = "Percentages for {}: {}"
        for i, image in enumerate(self.dataframe["after_image"]):
            print(percentage_string.format(image.image_name, image.image_data['percentages']))
            plt.subplot(size, size, i+1), plt.imshow(image["analyzed_image"], cmap = "RdYlGn"), plt.title(image.image_name)
        plt.subplots_adjust(wspace=0.2, hspace = 0.5)
        plt.show()
