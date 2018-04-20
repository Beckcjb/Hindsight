import sys
import math

import cv2
import pandas as pd
import numpy as np

from pandas.tools.plotting import table
from ..config import Config
from Source_Code import Image
from Source_Code import matlab
from .control_funcs import *

import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt

class Control:

    def __init__(self, file_list, basepath, rock_type, func_list, func_args, *args, **kwargs):
        self.dataframe = pd.DataFrame(columns = ['image_group',
                                                 'before_image',
                                                 'after_image',
                                                 'output_image'])
        self.func_list = func_list
        self.func_args = func_args
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
        rock_type = config.get_rock_type()
        func_list = config.get_run_list()
        func_args =config.get_arg_list()
        return cls(file_list, basepath, rock_type, func_list, func_args)

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
        count = 0
        for func in self.func_list:
            if func == "":
                continue
            elif func == "ml_color_segment":
                self.apply_func(func, rock_type = self.rock_type, ml_eng = matlab.matlab_engine)
            elif func == "analyze_mask":
                print(func)
                self.apply_func(func, analysis_func = self.func_args[0],
                                      buffer = self.func_args[6],
                                      center = (self.func_args[4], self.func_args[3]),
                                      radius = self.func_args[2],
                                      band_size = self.func_args[5])
            else:
                self.apply_func(func)

        #for multiple windows
        for i, image in enumerate(self.dataframe["after_image"]):
            fig = plt.figure()
            plt.subplot(1,2,1)
            plt.imshow(image["orig_image_data"], aspect="equal")
            plt.imshow(image["analyzed_image"], cmap = "RdYlGn", aspect="equal", alpha = .3)
            plt.title('Analyzed')
            plt.axis('off')
            plt.tight_layout()
            plt.subplot(1,2,2)
            plt.title('Original')
            plt.imshow(image["orig_image_data"], aspect="equal")
            plt.axis('off')
            plt.tight_layout()

            name = image.image_name[:11]
            after_number = image.image_name[12:18]
            fig.canvas.set_window_title( name + '_' + after_number)
            this_manager = plt.get_current_fig_manager()
            this_manager.window.wm_iconbitmap("logo.ico")
        plt.show()

    def save(self):
        for i, image in enumerate(self.dataframe["after_image"]):
            plt.figure()
            plt.subplot(111, frame_on=False) # no visible frame
            plt.axis('off')
            plt.imshow(image["analyzed_image"], cmap = "RdYlGn")
            name = image.image_name[:11]
            after_number = image.image_name[12:18]
            plt.savefig(self.basepath + '/' + name + after_number + '_result.png', bbox_inches='tight')
