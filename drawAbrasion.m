function abrasion = drawAbrasion(img_file)
% default values: xcor = 1110, ycor = 1135, radius = 320
% Move down: increase c_col; Move up: decrease c_col
% Move left: decrease c_row; Move right: increase c_row

% If the last three parameters were not given, then use the default values
 xcor = 1110;
 ycor = 1135;
 radius = 320;


img = imread(img_file);
ci = [xcor ycor radius]; % center and radius of circle ([c_row, c_col, r])
abrasion = insertShape(img, 'Circle', ci, 'LineWidth', 10);
end