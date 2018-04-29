function [fusedMask, fusedMaskedRGBImage] = combineRockEMask(RGB)

% Get the light mask of the image
[lightBW, lightMaskedImage] = dustELight(RGB);

% Get the dark mask of the image
[darkBW, darkMaskedImage] = rockEdustDark(RGB);

% If blend doens't work switch it back to 'diff
fusedMask = imfuse(lightBW, darkBW, 'blend');

fusedMaskedRGBImage = imfuse(lightMaskedImage, darkMaskedImage, 'blend');

end
