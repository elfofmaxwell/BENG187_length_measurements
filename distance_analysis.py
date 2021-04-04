import os
import cv2, time
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import init_processing


import single_image_distance, plot_figures, follow_log

dir_name = input("enter the path the images would be saved: \n") 


try: 
    os.mkdir(dir_name)
    print("Directory ", dir_name, "is created")
except FileExistsError: 
    print("Directory ", dir_name, "already exists") # create the path if it does not exist
    input('Enter to continue')

try: 
    os.mkdir(dir_name+'result/')
    print("Directory "+dir_name+'/restult/'+"is created")
except FileExistsError: 
    print("Directory "+dir_name+'/result/'+'already exists') # create the path if it does not exist
    input('Enter to continue')

with open(dir_name+'result/dist_log.txt', "w") as dist_log: 
    dist_log.write('time, dist, temp, pH,\n')
    print('distance log file created')

delay_time = int(input("enter the delay in second: \n")) # get the delay

input("press enter to start capture: ") # wait for starting


cap = cv2.VideoCapture(2) # start to cap
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 10000)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 10000)
for test_cam in range(4): 
    ret_test, frame_test = cap.read()
num_images = 0
distance_list = []
time_stamp = []
temp_list = []
ph_list = []
monitor = plot_figures.DynamicMonitor((2,2), (10,10))
temp_monitor = plot_figures.DisplayRange(monitor.axis[0])
ph_monitor = plot_figures.DisplayRange(monitor.axis[1])
dist_monitor = plot_figures.DisplayAll(monitor.axis[3])



while True: 
    try: 
        ret, frame = cap.read()
        cv2.imwrite(dir_name+'result/'+'%4.4d'%num_images+'.jpg', frame) # save the image
        frame_rotated = init_processing.rotate_image(frame, 270)
        frame_cropped = init_processing.crop_image(frame_rotated, (260,580), (530,1530))
        cv2.imwrite(dir_name+'result/'+'%4.4d'%num_images+'_crp.jpg', frame_cropped)
        frame_result = single_image_distance.SingleResult(frame_cropped) # create image_result object
        frame_result.save_result_image(dir_name+'result/processed_'+'%4.4d'%num_images+'.jpg')
        num_images += 1
        if num_images < 3: 
            continue
        distance_list.append(frame_result.measure_single_dist()) # append distance result
        time_stamp.append(num_images*delay_time/60.0) # append time stamp


        # read sensors
        sensor_log = follow_log.follow_log('D:\\se_ds\\ref\\ser_log.txt')
        sensor_log_sliced = follow_log.string_slicer(sensor_log)
        temp_list.append(float(sensor_log_sliced[1]))
        ph_list.append(float(sensor_log_sliced[2])) 

        # display all info
        temp_monitor.set_label(('Time (min)', 'Temperature'))
        temp_monitor.display_range(time_stamp, temp_list, 10)

        ph_monitor.set_label(('Time (min)', 'pH'))
        ph_monitor.display_range(time_stamp, ph_list, 10)
        
        dist_monitor.set_y_lim((400, 800))
        dist_monitor.set_label(('Time (min)', 'Distance'))
        dist_monitor.display_all(time_stamp, distance_list)

        # write into log file
        dist_record = time.strftime('%H:%M:%S, ')+str(distance_list[-1])+', '+str(temp_list[-1])+', '+str(ph_list[-1])+',\n'
        with open(dir_name+'result/dist_log.txt', 'a') as dist_log: 
            dist_log.write(dist_record)

        # sleep
        plt.pause(delay_time)

    # stop and release camera when ^c
    except KeyboardInterrupt: 
        cap.release()
        dist_log.close()
        break
