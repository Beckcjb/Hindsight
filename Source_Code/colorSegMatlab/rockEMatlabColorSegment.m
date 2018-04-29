function [BW, maskedRGBImage] = matlabColorSeg(Name)

image = imread(Name);

[BW, maskedRGBImage] = hsvDark(image);

end
