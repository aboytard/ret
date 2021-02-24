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
#
#@section todo
# Add the possibility for the user to erase the data that were on the database he is gonna use, if he is doing the same measurements than before.

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
        self.client = InfluxDBClient(host=self.parameter.influxdb_host,port=self.parameter.influxdb_port,username='ret', password='asdf', database=self.parameter.influxdb)
        self.time_button_entering_area = time.time()
        self.time_button_leaving_area = time.time()
        self.datetime_button_entering_area = datetime.datetime.utcnow()
        self.datetime_button_leaving_area = datetime.datetime.utcnow()
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
#                            self.parameter.BtnMasherApplication_output.print_end_effector_position_information()
                            self.datetime_button_entering_area = button_area.time_end_effector_entering_area 


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
                        self.datetime_button_leaving_area = button_area.time_end_effector_leaving_area
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
        t1 = datetime.datetime.strptime(str(self.parameter.time_Btn_pressed), '%Y-%m-%d %H:%M:%S.%f')
        t2 = datetime.datetime.strptime(str(self.parameter.time_Btn_unpressed), '%Y-%m-%d %H:%M:%S.%f')
        self.parameter.time_to_compare = t1 + (t2-t1)/2
        for button_area in self.parameter.list_buttons_area :
                if button_area.name == self.parameter.working_on_button:
                    if ((self.parameter.time_to_compare - button_area.time_end_effector_entering_area >= datetime.timedelta(0, 0, 0)) and 
                        (self.parameter.time_to_compare - button_area.time_end_effector_leaving_area <= datetime.timedelta(0, 0, 0)) ): 
                        success = True
                        self.parameter.list_to_log_RET = self.parameter.list_msg_change_state
                        self.parameter.list_to_log_csv.append(self.parameter.end_effector_position_entering_button_area)
                        self.parameter.list_to_log_csv.append(self.parameter.end_effector_position_received_socket_message_pressed)
                        self.parameter.list_to_log_csv.append(self.parameter.end_effector_position_leaving_button_area)
                        
                    else:
                        success = False
                        print ("time entering =", button_area.time_end_effector_entering_area)
                        print("time middle pressed = ", self.parameter.time_to_compare)
                        print ("time leaving =", button_area.time_end_effector_leaving_area)
                        if RET_config.real_time_processing:
                            RET_config.stop_thread = True
                            print("we are stopping the simulation because of an error of time detected")

        self.write_into_influxdb(self.client)
        self.write_json_influxdb_RET(self.client,success)
        self.write_into_csv_db(success)

    def write_into_influxdb(self,client):
        """! Retrieves the time the button where pressed detected by the Raspberri Pi.
        @parameter client The influxdb databases we want to log the data in.
        @return  Write the event of the button pressing inside the time interval in the Influxdb.
        """
        client.create_database(self.parameter.influxdb) 
        client.switch_database(self.parameter.influxdb)
        
    def write_json_influxdb_RET(self,client,success): 
        if success == True :
            request_type = "All"
        if success == False :
            request_type = "Error"
        json_body_RET = [
            {
                "measurement": self.parameter.influxdb_measurement_RET_info,
                "tags": {
                    "requestName": self.parameter.list_to_log_RET[1],
                    "requestType": request_type
                },
                "time": datetime.datetime.utcnow(),
                 "fields": {
                    "time_end_effector_entering": str(self.datetime_button_entering_area),
                    "time_button_pressed": str(self.parameter.time_Btn_pressed),
                    "time_compared": str(self.parameter.time_to_compare),
                    "time_button_unpressed": str(self.parameter.time_Btn_unpressed),
                   "time_end_effector_leaving": str(self.datetime_button_leaving_area)
                            }
            }
        ]
    
        json_body_RET_entering_time = [
            {
                "measurement": self.parameter.influxdb_measurement_RET_time_entering,
                "tags": {
                    "requestName": self.parameter.list_to_log_RET[1],
                    "requestType": request_type
                },
                "time": self.datetime_button_entering_area,
                 "fields": {
                    "time_end_effector_entering": True
                            }
            }
        ]    

        json_body_RET_pressing_time = [
            {
                "measurement": self.parameter.influxdb_measurement_RET_time_pressing,
                "tags": {
                    "requestName": self.parameter.list_to_log_RET[1],
                    "requestType": request_type
                },
                "time": self.parameter.time_Btn_pressed,
                 "fields": {
                    "time_pressing": True
                            }
            }
        ]      

        json_body_RET_comparing_time = [
            {
                "measurement": self.parameter.influxdb_measurement_RET_time_compared,
                "tags": {
                    "requestName": self.parameter.list_to_log_RET[1],
                    "requestType": request_type
                },
                "time": self.parameter.time_to_compare,
                 "fields": {
                    "time_comparing": True
                            }
            }
        ]      


        json_body_RET_unpressing_time = [
            {
                "measurement": self.parameter.influxdb_measurement_RET_time_unpressing,
                "tags": {
                    "requestName": self.parameter.list_to_log_RET[1],
                    "requestType": request_type
                },
                "time": self.parameter.time_Btn_unpressed,
                 "fields": {
                    "time_unpressing": True
                            }
            }
        ]        
        json_body_RET_leaving_time = [
            {
                "measurement": self.parameter.influxdb_measurement_RET_time_leaving,
                "tags": {
                    "requestName": self.parameter.list_to_log_RET[1],
                    "requestType": request_type
                },
                "time": self.datetime_button_leaving_area,
                 "fields": {
                    "time_end_effector_leaving": True
                            }
            }
        ]      
    
     
        client.write_points(json_body_RET)
        client.write_points(json_body_RET_entering_time)
        client.write_points(json_body_RET_pressing_time)
        client.write_points(json_body_RET_comparing_time)
        client.write_points(json_body_RET_unpressing_time)
        client.write_points(json_body_RET_leaving_time)
#        client.write_points(json_body_entering_button_area)
#        client.write_points(json_body_leaving_button_area)
        print("writing in Influxdb is made")
    
    def write_json_influxdb_additional_information(self,client):
        """! Retrieves additional data.
        @parameter client The influxdb databases we want to log the data in.
        @return  Write the additional data in the Influxdb.
        """
        ## add the other node for Ragesh
        pass
    
    def write_into_csv_db(self,success):
        """! Retrieves the csv logfile.
        @return  Write the RET data in the Influxdb.
        """      
        list_to_log = [datetime.datetime.utcnow(),self.parameter.list_to_log_RET[1],str(self.parameter.time_Btn_pressed),str(self.parameter.time_Btn_pressed),str(self.parameter.time_Btn_unpressed),str(self.datetime_button_leaving_area)]
        with open(self.parameter.csv_name_file,"aw") as f:
            cr = csv.writer(f,delimiter=",",lineterminator="\n")
            list_to_log.append(success)
            cr.writerow(list_to_log)
    
    def run(self):
        """! Retrieves RET_data_processing class.
        @return  Launch the thread that processes the data.
        """
        while RET_config.stop_thread == False:
           self.end_effector_inside_Btn_area()
           self.end_effector_outside_Btn_area()
        print("thread data_processing is closed")