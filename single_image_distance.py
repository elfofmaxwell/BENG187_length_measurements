'''
This file would have a class that describe a single image result, and should be 
able to give some most basic analysis results
'''
import cv2
import numpy as np

def remove_extra_cnt(countours): 
    '''
    countours: list of countours
    '''
    while len(countours) > 1: 
        if len(countours[0]) < len(countours[1]): 
            countours.pop(0)
        else: 
            countours.pop(1)
    
    return countours

def find_center(img): 
    '''
    this function find the center of a shape in given image
    img: np.array, binary image array opened with opencv

    output: 
    center_x: int, x coordination of the center
    center_y: int, y coordination of the center
    countours: list, list of all identified counters
    '''
    countours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    countours = remove_extra_cnt(countours)
    try: 
        cnt = countours[0]
        moment = cv2.moments(cnt)
    except IndexError: 
        print('Invalid image')
        center_x = -1
        center_y = -1

    else:
        try: 
            center_x = int(moment['m10']/moment['m00'])
            center_y = int(moment['m01']/moment['m00'])
        except ZeroDivisionError: 
            print('Invalid image')
            center_x = -1
            center_y = -1

    return center_x, center_y, countours

def measure_dist(img): 
    '''
    this function would automatically measure the distance between the center 
    of the blue region and red region inside the sample. 
    img: np.array object of sample image opened by opencv

    return: 
    dist: int, y-distance between center of the blue region and red region, in 
    pixels
    '''
    img_b, img_g, img_r = cv2.split(img) # split channels

    ret, img_r_binary = cv2.threshold(img_r, 175, 255, cv2.THRESH_BINARY)
    ret, img_g_binary = cv2.threshold(img_g, 127, 255, cv2.THRESH_BINARY) # binarilize
    ret, img_b_binary = cv2.threshold(img_b, 120, 255, cv2.THRESH_BINARY) 
    
    ret, img_r_mask = cv2.threshold(img_r, 105, 1, cv2.THRESH_BINARY_INV) 
    ret, img_g_mask_r = cv2.threshold(img_g, 185, 1, cv2.THRESH_BINARY_INV)
    ret, img_g_mask_b = cv2.threshold(img_g, 150, 1, cv2.THRESH_BINARY_INV) # binarilize mask
    ret, img_b_mask = cv2.threshold(img_b, 185, 1, cv2.THRESH_BINARY_INV) 

    img_r_final = cv2.multiply(cv2.multiply(img_r_binary, img_b_mask), img_g_mask_r)
    img_b_final = cv2.multiply(cv2.multiply(img_b_binary, img_r_mask), img_g_mask_b)
    center_r_x, center_r_y, contours_r = find_center(img_r_final)
    center_b_x, center_b_y, contours_b = find_center(img_b_final)

    if (center_b_y == -1) or (center_r_y == -1): 
        dist = 0
    else: 
        dist = center_b_y - center_r_y

    return dist, img_r_final, img_b_final, contours_r, contours_b, (center_r_x, center_r_y), (center_b_x, center_b_y)


def generate_zero_channel(size): 
    zero_channel = np.zeros(size, dtype='uint8')
    return zero_channel

def draw_result(img_r, img_b, contours_r, contours_b, center_r, center_b, result_path): 
    '''
    this function draw and save the proccessed images
    img_r: image array, grayscale, for red channel
    img_b: image array, grayscale, for blue channel
    contours_r: list of countour object of red channel
    contours_b: list of countour object of blue channel
    center_r: (x, y) tuple, coordination of red region center
    center_b: (x, y) tuple, coordination of blue region center
    result_path: string, path for resulted image
    '''
    zero_channel = generate_zero_channel(img_r.shape[:2])
    img_processed = cv2.merge([img_b, zero_channel, img_r])
    img_processed = cv2.drawContours(img_processed, contours_r, -1, (255, 255, 255), 3)
    img_processed = cv2.drawContours(img_processed, contours_b, -1, (255, 255, 255), 3)
    if (center_r[0] != -1) and (center_b[0] != -1): 
        img_processed = cv2.circle(img_processed, (center_r[0], center_r[1]), 5, (255, 255, 255), -1)
        img_processed = cv2.circle(img_processed, (center_b[0], center_b[1]), 5, (255, 255, 255), -1)

    cv2.imwrite(result_path, img_processed)

class SingleResult(): 
    '''
    This is the class for single image result. 
    image_path: string for path of image
    '''
    def __init__(self, image): 
        '''
        image: opencv array
        '''
        self.img = image
        

    def measure_single_dist(self): 
        '''
        return: 
        distance: int, y-distance between center of the blue region and red region, in 
        pixels
        '''
        dist = measure_dist(self.img)
        distance = dist[0]
        return distance

    def save_result_image(self, result_path): 
        '''
        result_path: string
        '''
        dist, img_r, img_b, contours_r, contours_b, center_r, center_b = measure_dist(self.img)
        draw_result(img_r, img_b, contours_r, contours_b, center_r, center_b, result_path)


    
