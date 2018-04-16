def normalize_func(row, newMin = 0, newMax = 1):
    row['before_image'].normalize_image(newMin = newMin, newMax = newMax)
    row['after_image'].normalize_image(newMin = newMin, newMax = newMax)

def subtract_func(row, *args, data = 'orig_image_data', useNorm = True, **kwargs):
    row['after_image'].subtract(row['before_image'], *args, data = data, useNorm = useNorm, **kwargs)

def convert_func(row, from_image, to_image, conversion_type):
    row['before_image'].convert(from_image, to_image, conversion_type)
    row['after_image'].convert(from_image, to_image, conversion_type)

def analyze_mask_func(row, mask = "color_mask", analysis_func = "circular", buffer = 30):
    image = row['after_image']
    masks = {'color_mask': image['color_mask']}

    try:
        mask = masks[mask]
    except:
        raise KeyError('The mask ' + mask + ' does not exist.')
    if(analysis_func == "block"):
        image.analyze_mask_block(mask, buffer = buffer)
    elif(analysis_func == "circular"):
        image.analyze_mask_circlular(mask, buffer = buffer)

def color_segment_func(row, rock_type):
    image = row['after_image']
    image.color_segment(rock_type)

def ml_color_segment_func(row, ml_eng):
    image = row['after_image']
    image_path = row['after_image'].image_path
    image.ml_color_segment(image_path, ml_eng)
