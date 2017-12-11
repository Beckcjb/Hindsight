[image1, usercancelled1] = imgetfile();
[image2, usercancelled2] = imgetfile();
[image3, usercancelled3] = imgetfile();

[bw1, rgb1] = createMask2(imread(image1));
[bw2, rgb2] = createMask2(imread(image2));
[bw3, rgb3] = createMask2(imread(image3));

figure; imshow(rgb1);
figure; imshow(bw1);

figure; imshow(rgb2);
figure; imshow(bw2);

figure; imshow(rgb3);
figure; imshow(bw3);

%{
derp = imread('after.jpg');
[bw, rgb] = createMask(derp);

figure;
imshow(rgb);
figure; imshow(bw);
derp2 = imread('before.jpg');
[bw2, rgb2] = createMask2(derp2);

figure;
imshow(rgb2);

figure;
imshow(bw2);
%}