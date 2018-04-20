function [BW, maskedRGBImage] = matlabColorSeg(Name)

image = imread(Name);

[BW, maskedRGBImage] = createMask2(image);

end
