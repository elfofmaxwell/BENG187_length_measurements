# BENG187_length_measurements
This repository contains all codes that are used in Senior Design Project of 2021 year Group 13, Department of Bioengineering, UC San Diego. 

* arduino_code.ino contains the codes running on a arduino board. It works to read temperature, control the heater through a relay, and read pH probe's out put (0-1024)
* follow_log.py, init_processing.py, plot_figures.py, set_figure_area.py, single_image_distance.py contain modulus to be used. pyplotlib, opencv-python, numpy, pyserial are required. 
* find_cam is used to find the index of the camera when multiple cameras exist. 
* distance_analysis is the main script for taking pictures and image analysis. 
* serial_reader.py is the script that read the data sent from arduino. It also convert pH probe results 0-1024 to formatted 0-14 pH value. 
