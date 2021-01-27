#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 15:40:24 2021

@author: ret
"""

# @file RET.py
#
# @brief Defines the global variable that the RET is using.
#
# @section RET_config Description
# Define the global variable that the RET is using on the computer:
# - the possibility of real time processing
# - the possibiliy of stopping the thread when the test is ended
# - the global variable for the socket communication
# - the definition of the button's areas we are working with
# - the databases we are logging the data in
#
# @section libraries_RET_config Libraries/Modules
# - datetime 

import datetime 
import time

real_time_processing = True
stop_thread = False   

## global variable for the socket communication
socket_host = '10.4.11.117'
socket_port = 5003

## global variable for the data storage
influxdb_host="localhost"
influxdb_port="8086"
influxdb = "RET_Test"

## global variable for csv logfile


## global variable to test
robot_settle_time = 0.01
acceleration_factor = 1.7
velocity_factor = 1.57
minimal_time_interval_button_area = time.time() ### introduce the time from the experiment 2*(mean(time push/unpushed)+time message socket send/receive))

class Btn():
    """! The Btn base class.
    Defines the base class utilized by all buttons.
    """
    def __init__(self,name,x,y,z):
        """! The Btn base class initializer.
        @param name  The name of the Btn.
        @param x  The x coordinate of the button.
        @param y  The y coordinate of the button.
        @param z  The z coordinate of the button.
        @return  An instance of the Btn class initialized with the specified name.
        """
        self.name = name
        self.x = x
        self.y = y
        self.z = z
    
class Btn_area(Btn):
    """! The Btn_area class.
    Provide access to the button_area's.
    """
    def __init__(self,Btn,dx,dy,dz):
        """! The Btn_area base class initializer.
        @param Btn  The Btn we are defining the area of.
        @param dx  The delta on x we are defining for the button area.
        @param dy  The delta on y we are defining for the button area.
        @param dz  The delta on z we are defining for the button area.
        @return  An instance of the Btn_area class initialized with the specified name.
        """
        self.name = Btn.name
        self.x = Btn.x
        self.y = Btn.y
        self.z = Btn.z
        self.dx = dx
        self.dy = dy
        self.dz = dz
        self.upper_x = Btn.x + dx
        self.upper_y = Btn.y + dy
        self.upper_z = Btn.z + dz
        self.lower_x = Btn.x - dx
        self.lower_y = Btn.y - dy
        self.lower_z = Btn.z - dz  
        self.end_effector_inside_area = False
        self.send_message_entering_area = False
        self.time_end_effector_entering_area = datetime.datetime.utcnow()
        self.send_message_leaving_area = False
        self.time_end_effector_leaving_area = datetime.datetime.utcnow()
 
 ## definition of the buttons
delta_area = [0.06,0.05,0.02]    
x1 = -0.1
y1 = -0.45
z1 = 0.159
x2 = 0.05
y2 = -0.45
z2 = 0.159
Btn1 = Btn("Btn1",x1,y1,z1)
Btn2 = Btn("Btn2",x2,y2,z2)

Btn1_area = Btn_area(Btn1, delta_area[0], delta_area[1], delta_area[2])
Btn2_area = Btn_area(Btn2, delta_area[0], delta_area[1], delta_area[2])

list_buttons_area = [Btn1_area,Btn2_area]

### log into csv
#csv_name_file = ("RET_csv_logfile/"+ button_names + str(list_buttons_positions) + "["+ str(list_buttons_area[0].dx) + ";" + str(list_buttons_area[0].dy) + ";"  + 
#str(list_buttons_area[0].dz) + "]_bouncetime_" + str(list_bouncetime) +"_acceleration_factor_[" + str(acceleration_factor) +"]_velocity_factor_["+ str(velocity_factor) + "]_robot_settle_time_"+
#str(robot_settle_time) + "]_ROS.csv")
#
#with open(self.csv_name_file,"aw") as csv_file:
#    writer = csv.writer(csv_file,delimiter=";",lineterminator="\n")
#    writer.writerow(self.csv_header)