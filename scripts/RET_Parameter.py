#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 09:39:02 2021

@author: ret
"""

import datetime
import Button_Masher_Application_Output
import RET_config
import csv

########## The input of this function is the cartesian position of the end effector given by another node!!!!!!!!!!!!!!!

class RET_Parameter(Button_Masher_Application_Output.Button_Masher_Application_node_listener):
    def __init__(self,ButtonMasherApplication_output,list_buttons_area):
        self.test = False
        #### Global Parameter of the RET
        self.time_begin_RET = datetime.datetime.utcnow()
        self.RET_driver = ""
        self.acceleration_factor = RET_config.acceleration_factor
        self.velocity_factor = RET_config.velocity_factor
        self.robot_settle_time = RET_config.robot_settle_time
        self.list_buttons_area = list_buttons_area
        #### Parameter about the Button Masher Application output
        self.BtnMasherApplication_output = ButtonMasherApplication_output
        ##changing parameter
        self.working_on_button = ""
        self.time_End_Effector_entering_Btn_Area = datetime.datetime.utcnow()
        self.time_End_Effector_leaving_Btn_Area = datetime.datetime.utcnow()
        self.Btn_Pressed_Time = datetime.datetime.utcnow()
        #### Parameter concerning the socket message
        ##static parameter
        self.socket_host = RET_config.socket_host
        self.socket_port = RET_config.socket_port
        ##changing parameter
        self.list_msg_Btn_Pressed = []
        self.time_Btn_Pressed = datetime.datetime.utcnow()
        self.list_to_log = []
        #### Parameter concerning the influxdb writing
        ## static parameter
        self.influxdb_host = RET_config.influxdb_host
        self.influxdb_port = RET_config.influxdb_port
        self.influxdb = RET_config.influxdb
        ## information about the measurement
        self.button_names= ""
        self.list_bouncetime = []
        self.list_buttons_positions=[]
        for button_area in self.list_buttons_area:
            list_button_positions = []
            self.button_names += button_area.name + "_"
            list_button_positions.append(button_area.x)
            list_button_positions.append(button_area.y)
            list_button_positions.append(button_area.z)
            self.list_bouncetime.append(button_area.bouncetime)
            self.list_buttons_positions.append(list_button_positions)
        self.influxdb_measurement = ( "RET_Test" + self.button_names + str(self.list_buttons_positions) + "["+ str(self.list_buttons_area[0].dx) + ";" + str(self.list_buttons_area[0].dy) + ";"  + 
        str(self.list_buttons_area[0].dz) + "]_bouncetime_" + str(self.list_bouncetime) +"_acceleration_factor_[" + str(self.acceleration_factor) +"]_velocity_factor_["+ str(self.velocity_factor) + "]_robot_settle_time_"+
        str(self.robot_settle_time) + "]_ROS")
        print ("The database in influx db is named: ", self.influxdb)
        print("Data are logged in the next measurements:",self.influxdb_measurement)
        ##### parameter for writing csv_file
        self.csv_name_file = (self.button_names + str(self.list_buttons_positions) + "["+ str(self.list_buttons_area[0].dx) + ";" + str(self.list_buttons_area[0].dy) + ";"  + 
        str(self.list_buttons_area[0].dz) + "]_bouncetime_" + str(self.list_bouncetime) +"_acceleration_factor_[" + str(self.acceleration_factor) +"]_velocity_factor_["+ str(self.velocity_factor) + "]_robot_settle_time_"+
        str(self.robot_settle_time) + "]_ROS.csv")
        self.csv_header =  ['datetime.utcnow','Btn_name','Action','In_Time_Interval']
        self.open_csv_file()
        
    def open_csv_file(self):
        with open('/home/ret/workspaces/ret/src/ret/scripts/RET_csv_logfile/'+self.csv_name_file,"w") as f:
            cr = csv.writer(f,delimiter=";",lineterminator="\n")
            cr.writerow(self.csv_header)
  