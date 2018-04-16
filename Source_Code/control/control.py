
import sys
import pandas as pd
import cv2
import numpy as np


from pandas.tools.plotting import table
from ..config import Config
from Source_Code import Image
from .control_funcs import subtract_func, color_segment_func, analyze_mask_func

import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt

class Control:

    def __init__(self, file_list, basepath, func_list, rock_type,  edge_value_x, edge_value_y, 
                    edge_value_radi, band_size, buffer, analysis_option, *args, **kwargs):
        self.dataframe = pd.DataFrame(columns = ['image_group','before_image','after_image','output_image'])
        self.func_list = func_list
        self.rock_type = rock_type
        self.basepath = basepath
        self.file_list = file_list
        self.edge_value_x = edge_value_x
        self.edge_value_y = edge_value_y
        self.edge_value_radi = edge_value_radi
        self.buffer = buffer
        self.band_size = band_size
        self.analysis_option = analysis_option
 
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
        edge_value_x = config.get_abrasionX()
        edge_value_y = config.get_abrasionY()
        edge_value_radi = config.get_abrasion_radius()
        buffer = config.get_buffer()
        band_size = config.get_band_size()
        analysis_option = config.get_analysis_option()
        return cls(file_list, basepath, func_list, rock_type, edge_value_x, edge_value_y, 
                    edge_value_radi, band_size, buffer, analysis_option)

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
    
        count = 0
        for func in self.func_list:
            if func == "color_segment":
                self.apply_func(func, rock_type = self.rock_type)
            else if func =="None":
                pass
            else:
                self.apply_func(func)

        self.after_images = []
        for i, elem in enumerate(self.file_list):
            if 'af' in elem:
                self.after_images.append(elem)
        
        #for multiple windows
        for i, image in enumerate(self.dataframe["after_image"]):
            fig = plt.figure()
            plt.subplot(1,2,1)
            plt.imshow(image["analyzed_image"], cmap = "RdYlGn", aspect="equal") 
            plt.title('Analyzed')
            plt.axis('off')        
            plt.tight_layout()
            plt.subplot(1,2,2)
            plt.title('Original')
            plt.imshow(image["orig_image_data"], aspect="equal")  
            plt.axis('off')
            plt.tight_layout()
            name = self.after_images[i][:11]
            afterNumber = self.after_images[i][12:18]
            fig.canvas.set_window_title( name + '_' + afterNumber)
            thismanager = get_current_fig_manager()
            thismanager.window.wm_iconbitmap("logo.ico")
        plt.show()
        
    def save(self):
        for i, image in enumerate(self.dataframe["after_image"]):
            plt.figure()
            plt.subplot(111, frame_on=False) # no visible frame
            plt.axis('off')
            plt.imshow(image["analyzed_image"], cmap = "RdYlGn")
            name = self.after_images[i][:11]
            afterNumber = self.after_images[i][12:18]
            plt.savefig(self.basepath + '/' + name + afterNumber + '_result.png', bbox_inches='tight')
