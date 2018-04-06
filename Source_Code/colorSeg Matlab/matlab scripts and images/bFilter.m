clc;
close all;

[image1, usercancelled1] = imgetfile();
[image2, usercancelled2] = imgetfile();

im1 = imread(image1);
im2 = imread(image2);

% do image subtraction
figure; imshow(im2-im1);

[bw1, rgb1] = bMaskTest(im1);
[bw1_2, rgb1_2] = DustBMask(im1);
figure; imshow(rgb1);
figure; imshow(rgb1_2);

figure;

rgb1 = imcrop(im1);
rgb2 = imcrop(im1);
rgb3 = imcrop(im1);

[X, map] = rgb2ind(rgb1, 2048);
[X2, map2] = rgb2ind(rgb2, 2048);
[X3, map3] = rgb2ind(rgb3, 2048);

[hist1, x] = imhist(X, map);
[hist2, x2] = imhist(X2, map2);
[hist3, x3] = imhist(X3, map3);

% normalize

hist1 = hist1/sum(hist1);
hist2 = hist2/sum(hist2);
hist3 = hist3/sum(hist3);

figure; plot(x, hist1, x2, hist2, x3, hist3); legend('Dust', 'Also dust', 'not dust');
%{
figure; plot(hist1); title('Dust'); 
figure; plot(hist2); title('Also Dust');
figure; plot(hist3); title('Not Dust');
%}

%{
d = pdist2(hist1, hist2);
d2 = pdist2(hist1, hist3);
%}

%{
%get hist values for each channel
[R, x] = imhist(Red);
%figure; imshow(yRed);
[G, x] = imhist(Green);
[B, x] = imhist(Blue);
figure;
imshow(R);
figure;
imshow(G);
figure;
imshow(B);
%}

%{
figure; histcounts(rgb1);
figure; imshow(rgb1);
%}

%{
[X, map] = rgb2ind(im1, 64);
[X1, map1] = rgb2ind(im2, 64);

figure; imhist(X, map);
figure; imhist(X1, map1);
%}
%{
%j = stdfilt(im1);
%j2 = stdfilt(im2);
j = entropyfilt(im1);
j2 = entropyfilt(im2);

figure; imshow(j);
figure; imshow(j2);
%}
%{
B = imgaussfilt3(imread(image1), 5);
B2 = imgaussfilt3(imread(image2), 5);

derp = rgb2gray(B2-B);
derp = imbinarize(derp);

derp2 = rgb2gray(im2-im1);
derp2 = imbinarize(derp2);

figure; imshow(derp);
figure; imshow(derp2);
%j = entropyfilt(gi);

%figure; imshow(j);
%j2 = entropypfilt(image2);
%}