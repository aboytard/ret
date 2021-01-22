#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 09:39:02 2021

@author: ret
"""

import datetime
import Button_Masher_Application_Output

########## The input of this function is the cartesian position of the end effector given by another node!!!!!!!!!!!!!!!

class RET_Parameter(Button_Masher_Application_Output.Button_Masher_Application_node_listener):
    def __init__(self,ButtonMasherApplication_output,list_buttons_area):
        #### Global Parameter of the RET
        self.time_begin_RET = datetime.datetime.utcnow()
        self.RET_driver = ""
        self.list_buttons_area = list_buttons_area
        #### Parameter about the Button Masher Application output
        self.BtnMasherApplication_output = ButtonMasherApplication_output
        ##changing parameter
        self.time_End_Effector_entering_Btn_Area = datetime.datetime.utcnow()
        self.time_End_Effector_leaving_Btn_Area = datetime.datetime.utcnow()
        self.Btn1_send_information = False
        self.Btn2_send_information = False
        self.Btn_Pressed_Time = datetime.datetime.utcnow()
        #### Parameter concerning the socket message
        ##static parameter
        self.socket_host = '10.4.11.117'
        self.socket_port = 5011
        ##changing parameter
        self.list_msg_Btn_Pressed = []
        self.time_Btn_Pressed = datetime.datetime.utcnow()
        
        