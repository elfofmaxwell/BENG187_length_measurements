import cv2
import numpy as np

def rotate_image(img, angle): 
    (height, width) = img.shape[:2]
    (center_x, center_y) = (width/2, height/2)

    M = cv2.getRotationMatrix2D((center_x, center_y), -angle, 1.0)

    cos = np.abs(M[0,0])
    sin = np.abs(M[0,1])
    
    # 计算图像旋转后的新边界
    new_width = int((height*sin)+(width*cos))
    new_height = int((height*cos)+(width*sin))
    
    # 调整旋转矩阵的移动距离（t_{x}, t_{y}）
    M[0,2] += (new_width/2) - center_x
    M[1,2] += (new_height/2) - center_y
    
    return cv2.warpAffine(img,M,(new_width,new_height))

def crop_image(img, x_range, y_range): 
    img_cropped = img[y_range[0]:y_range[1], x_range[0]:x_range[1]]
    return img_cropped

