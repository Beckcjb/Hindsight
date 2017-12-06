import pandas as pd
from image.image import Image

class Control:

    def __init__(self, before_image, after_image, basepath, *args, **kwargs):
        # Loads a list of images and their associated pairs
        self.dataframe = pd.DataFrame(data = {'image_group': before_image,
                                              'before_image': [Image(basepath, before_image, *args, **kwargs)],
                                              'after_image':  [Image(basepath, after_image, *args, **kwargs)],
                                              'output_image': [None]})

    def add_image_pair(self, before_image, after_image, basepath, *args, **kwargs):
        new_pair = pd.DataFrame(data = {'image_group': before_image,
                                        'before_image': [Image(basepath, before_image, *args, **kwargs)],
                                        'after_image':  [Image(basepath, after_image, *args, **kwargs)],
                                        'output_image': [None]})
        self.dataframe = pd.concat([self.dataframe, new_pair], ignore_index=True)

    def apply_func(self, func, *args, **kwargs):
        self.dataframe.apply(func, axis = 1, *args, **kwargs)
