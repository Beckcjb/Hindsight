import sys
def normalize_func(row, newMin = 0, newMax = 1):
    row['before_image'].normalize_image(newMin = newMin, newMax = newMax)
    row['after_image'].normalize_image(newMin = newMin, newMax = newMax)

# Func needs work but the concept is there
def subtract_func(row, *args, data = 'orig_image_data', useNorm = True, **kwargs):
    row['after_image'].subtract(row['before_image'], *args, data = data, useNorm = useNorm, **kwargs)

def convert_func(row, from_image, to_image, conversion_type):
    row['before_image'].convert(from_image, to_image, conversion_type)
    row['after_image'].convert(from_image, to_image, conversion_type)

def analyze_mask_func(row, mask = "color_mask", buffer = 10):
    image = row['after_image']
    masks = {'color_mask': image['color_mask']}

    try:
        mask = masks[mask]
    except:
        raise KeyError('The mask' + mask + 'does not exist.')

    image.analyze_mask(mask, buffer = buffer)

def color_segment_func(row, rock_type):
    image = row['after_image']
    image.color_segment(rock_type)

def matlab_color_segment():
    print('banana')
