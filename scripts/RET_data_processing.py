#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 12:50:30 2021

@author: ret
"""

# @file RET_data_processing.py
#
# @brief Defines the RET_data_processing class.
#
# @section RET_data_processing Description
# Define the base and end parameter we are processing during the RET
#
# @section libraries_RET_data_processing Libraries/Modules
# - standard modules : enable to use python with ROS
#       - threading
#       - datetime
#       - InfluxDBClient
#       - csv
#       - time
# -custom class :
#       - RET_Parameter
#       - Btn_area defined in RET_config

import RET_Parameter
import RET_config

import threading
import datetime
from influxdb import InfluxDBClient
import csv
import time

class RET_data_processing(threading.Thread,RET_Parameter.RET_Parameter):
    """! The RET_data_processing class.
    Provides access to the processing of the data in the RET.
    """
    def __init__(self,parameter):
        """! The RET_data_processing class initializer.
        @param parameter  The parameter of the RET we are processing that includes the data we work with.
        @return  A thread instance that process the data while the RET is running.
        """
        threading.Thread.__init__(self)
        self.parameter = parameter
        ## add a parameter that determine which button we have to work on, instead of working on every button of the list anytime
        self.len_list_buttons_area = len(self.parameter.list_buttons_area)
        self.working_on_button = ""
        ## settle arguments to deal only with one Btn at the time, we cannot process every button of the list anytime
        self.inside_one_button_area = False
        self.process_data = False
        ## argument for Influxdb
        self.client = InfluxDBClient(host=self.parameter.influxdb_host,port=self.parameter.influxdb_port)
        self.time_button_entering_area = time.time()
        self.time_button_leaving_area = time.time()
        pass
    
    def end_effector_inside_Btn_area(self):
        """! Retrieves the end effector cartesian position description.
        @return  The event of the end effector entering a button's area.
        """
        #return the time the end effector enter the button area
        if self.inside_one_button_area == False:
            for button_area in self.parameter.list_buttons_area :
                    if button_area.end_effector_inside_area == False :
                        if ((button_area.lower_x < self.parameter.BtnMasherApplication_output.x < button_area.upper_x ) and
                            (button_area.lower_y < self.parameter.BtnMasherApplication_output.y < button_area.upper_y ) and 
                            (button_area.lower_z < self.parameter.BtnMasherApplication_output.z < button_area.upper_z)):
                            self.time_button_entering_area = time.time()
                            button_area.end_effector_inside_area = True
                            self.inside_one_button_area = True
                            self.parameter.working_on_button = button_area.name 
                            button_area.time_end_effector_entering_area = datetime.datetime.utcnow()
                            self.parameter.end_effector_position_entering_button_area = [str(button_area.time_end_effector_entering_area),self.parameter.BtnMasherApplication_output.x,self.parameter.BtnMasherApplication_output.y,self.parameter.BtnMasherApplication_output.z]
                            button_area.send_message_entering_area = True
                            print ("we have enter the area of : ", button_area.name)
                            self.parameter.BtnMasherApplication_output.print_end_effector_position_information()


    def end_effector_outside_Btn_area(self):
        """! Retrieves the end effector cartesian position description.
        @return  The event of the end effector leaving a button's area.
        """
        if self.inside_one_button_area == True:
            for button_area in self.parameter.list_buttons_area :
                if button_area.name == self.parameter.working_on_button and button_area.end_effector_inside_area == True:
                    if((button_area.lower_x > self.parameter.BtnMasherApplication_output.x or self.parameter.BtnMasherApplication_output.x > button_area.upper_x ) or
                       (button_area.lower_y > self.parameter.BtnMasherApplication_output.y or self.parameter.BtnMasherApplication_output.y > button_area.upper_y ) or 
                       (button_area.lower_z > self.parameter.BtnMasherApplication_output.z or self.parameter.BtnMasherApplication_output.z > button_area.upper_z)):
                        self.time_button_leaving_area = time.time()
                        button_area.end_effector_inside_area = False
                        button_area.end_effector_inside_area = False
                        print ("we have left the area of : ", button_area.name)
                        self.inside_one_button_area = False
                        button_area.time_end_effector_leaving_area = datetime.datetime.utcnow()
                        self.parameter.end_effector_position_leaving_button_area = [str(button_area.time_end_effector_leaving_area),self.parameter.BtnMasherApplication_output.x,self.parameter.BtnMasherApplication_output.y,self.parameter.BtnMasherApplication_output.z]
                        button_area.send_message_leaving_area = True
                        self.parameter.time_inside_button_area = self.time_button_leaving_area - self.time_button_entering_area
                        self.process_time_Btn_pressed()
#                        self.parameter.BtnMasherApplication_output.print_end_effector_position_information()


    
    def process_time_Btn_pressed(self):
        """! Retrieves the time the button where pressed detected by the Raspberri Pi.
        @return  The event of the time the button pressed inside the interval of time the 
        button is entering and leaving the button area or not.
        """
        ## process the time of the button is pressed with the time the button enter and leave the button area
        for button_area in self.parameter.list_buttons_area :
                if button_area.name == self.parameter.working_on_button:
                    if ((self.parameter.time_Btn_Pressed - button_area.time_end_effector_entering_area >= datetime.timedelta(0, 0, 0)) and 
                        (self.parameter.time_Btn_Pressed - button_area.time_end_effector_leaving_area <= datetime.timedelta(0, 0, 0)) ): 
                        self.parameter.list_to_log = self.parameter.list_msg_Btn_Pressed
                        self.parameter.list_to_log.append(True)
                        self.parameter.list_to_log.append(self.parameter.end_effector_position_entering_button_area)
                        self.parameter.list_to_log.append(self.parameter.end_effector_position_received_socket_message_pressed)
                        self.parameter.list_to_log.append(self.parameter.end_effector_position_leaving_button_area)
                    else:
                        print ("time entering =", button_area.time_end_effector_entering_area)
                        print("time pressed = ", self.parameter.time_Btn_Pressed)
                        print ("time leaving =", button_area.time_end_effector_leaving_area)
                        print("we are stopping the simulation because of an error of time detected")
                        if RET_config.real_time_processing:
                            RET_config.stop_thread = True
                        self.parameter.list_to_log = self.parameter.list_msg_Btn_Pressed
                        self.parameter.list_to_log.append(False)
                        self.parameter.list_to_log.append(self.parameter.end_effector_position_entering_button_area)
                        self.parameter.list_to_log.append(self.parameter.end_effector_position_received_socket_message_pressed)
                        self.parameter.list_to_log.append(self.parameter.end_effector_position_leaving_button_area)
        self.write_into_influxdb(self.client)
        self.write_json_influxdb_RET(self.client)
        self.write_into_csv_db()
    
    def write_into_influxdb(self,client):
        """! Retrieves the time the button where pressed detected by the Raspberri Pi.
        @parameter client The influxdb databases we want to log the data in.
        @return  Write the event of the button pressing inside the time interval in the Influxdb.
        """
        client.create_database(self.parameter.influxdb) 
        client.switch_database(self.parameter.influxdb)

    def write_json_influxdb_RET(self,client): 
        json_body = [
            {
                "measurement": self.parameter.influxdb_measurement,
                "tags": {
                    "requestName": "All_Information",
                    "requestType": "GET"
                },
                "time":self.parameter.list_to_log[0],#datetime.datetime.utcnow(),
                 "fields": {
                    "Btn_name": self.parameter.list_to_log[1], 
                    "Action": self.parameter.list_to_log[2],
                    "In_Time_Interval": self.parameter.list_to_log[3], 
                    "end_effector_position_entering_button_area": str(self.parameter.list_to_log[4]),
                    "end_effector_position_received_socket_message_pressed": str(self.parameter.list_to_log[5]),
                    "end_effector_position_leaving_button_area": str(self.parameter.list_to_log[6])
                            }
            }
        ]
        client.write_points(json_body)
        print("writing in Influxdb is made")
    
    def write_json_influxdb_additional_information(self,client):
        """! Retrieves additional data.
        @parameter client The influxdb databases we want to log the data in.
        @return  Write the additional data in the Influxdb.
        """
        ## add the other node for Ragesh
        pass
    
    def write_into_csv_db(self):
        """! Retrieves the csv logfile.
        @return  Write the RET data in the Influxdb.
        """
        with open('/home/ret/workspaces/ret/src/ret/scripts/RET_csv_logfile/'+self.parameter.csv_name_file,"aw") as f:
            cr = csv.writer(f,delimiter=",",lineterminator="\n")
            cr.writerow(self.parameter.list_to_log)
    
    def run(self):
        """! Retrieves RET_data_processing class.
        @return  Launch the thread that processes the data.
        """
        while RET_config.stop_thread == False:
           self.end_effector_inside_Btn_area()
           self.end_effector_outside_Btn_area()
        print("thread data_processing is closed")