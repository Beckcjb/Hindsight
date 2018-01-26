import cv2
from utils import utils

class Image:

    def __init__(self, basepath, image, readType = 1):
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

    def convert(self, from_image, to_image, conversion_type):
         self.image_data[to_image] = cv2.cvtColor(self.image_data[from_image], conversion_type)

    def generate_mask_image(self, buffer, path, name):
        y_val, x_val = self.xy_extent()
        point_values = self.mask_df.point_value

        mean_image = []
        iterator = 0

        for i in range(0, x_val, buffer):
            mean_sample = []
            for j in range(0, y_val, buffer):
                mean_sample.append(map_percentage(point_values[iterator]))
                iterator += 1
            mean_image.append(np.array(mean_sample))

        mask_image = os.path.join(path, name + '_test.png')
        cv2.imwrite(mask_image, np.array(mean_image))
        dist_image = cv2.imread(mask_image, 1)
        dist_image = cv2.cvtColor(dist_image, cv2.COLOR_BGR2RGB)
        dsize = self.xy_extent() + buffer
        dsize = (dsize[0], dsize[1])
        dist_image = cv2.resize(dist_image, dsize, fx=0, fy=0, interpolation = cv2.INTER_CUBIC)
        cv2.imwrite(mask_image, dist_image)
        return Image(path, name + '_test.png')
