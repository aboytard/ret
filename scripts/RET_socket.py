#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 12:16:16 2021

@author: ret
"""

# @file RET_socket.py
#
# @brief Defines the Computer_SocketClient_RET class.
# @brief Defines the Computer_ReceiveMessage_Rpi class.
# @brief Defines the Computer_SendMessage_Rpi class.
#
# @section RET_data_processing Description
# Define the base and end parameter we are processing during the RET
#
# @section libraries_RET_socket Libraries/Modules
# - standard modules : enable to use python with ROS
#       - threading
#       - datetime
#       - socket
#       - sys
# -custom class :
#       - RET_Parameter
#       - Btn_area defined in RET_config

import RET_Parameter
import socket,sys,threading
import RET_config
import datetime


class Computer_ReceiveMessage_Rpi(threading.Thread,RET_Parameter.RET_Parameter):
    """! The Computer_ReceiveMessage_Rpi RET class.
    Provides access to the message sent by the Raspberri Pi.
    """
    def __init__(self,parameter,connection):
        """! The Computer_ReceiveMessage_Rpi class initializer.
        @param parameter  The parameter we are working with.
        @param connection  The connection to the socket's server on the Raspberri Pi.
        @return  An instance of the Computer_ReceiveMessage_Rpi class initialized with the specified name.
        """
        threading.Thread.__init__(self)
        self.parameter = parameter
        self.connection = connection
    
    def run(self):
        """! Retrieves Computer_ReceiveMessage_Rpi description.
        @return  A thread that runs during the RET.
        """
        while RET_config.stop_thread == False:
            received_message = self.connection.recv(1024)
            print "*" + received_message + "*"
            if received_message == "":
                print("We received a "" message so we stop the socket communication")
                RET_config.stop_thread = True
            try:
                self.parameter.list_msg_Btn_Pressed = received_message.split(";")
                time_to_process = self.parameter.list_msg_Btn_Pressed[0]
                if self.parameter.list_msg_Btn_Pressed[2] == "pressed":
                    self.parameter.time_Btn_pressed = datetime.datetime.strptime(time_to_process, '%Y-%m-%d %H:%M:%S.%f')
                    self.parameter.end_effector_position_received_socket_message_pressed = [self.parameter.time_Btn_pressed,self.parameter.BtnMasherApplication_output.x,self.parameter.BtnMasherApplication_output.y,self.parameter.BtnMasherApplication_output.z]
#                        print (self.parameter.time_Btn_Pressed)
#                        print(self.list_msg_Btn_Pressed)
#                        print(self.parameter.BtnMasherApplication_output.x)
                if self.parameter.list_msg_Btn_Pressed[2] == "unpressed":
                    self.parameter.time_Btn_unpressed = datetime.datetime.strptime(time_to_process, '%Y-%m-%d %H:%M:%S.%f')
                    self.parameter.end_effector_position_received_socket_message_unpressed = [self.parameter.time_Btn_unpressed,self.parameter.BtnMasherApplication_output.x,self.parameter.BtnMasherApplication_output.y,self.parameter.BtnMasherApplication_output.z]
            except:
                pass
        self.connection.close()


class Computer_SendMessage_Rpi(threading.Thread,RET_Parameter.RET_Parameter):
    """! The Computer_SendMessage_Rpi RET class.
    Provides the possibility to send messages to the Raspberri Pi.
    """
    def __init__(self,parameter,connection):
        """! The Computer_SendMessage_Rpi class initializer.
        @param parameter  The parameter we are working with.
        @param connection  The connection to the socket's server on the Raspberri Pi.
        @return  An instance of the Computer_SendMessage_Rpi class initialized with the specified name.
        """
        threading.Thread.__init__(self)
        self.parameter = parameter
        self.list_msg_send = []
        self.connection = connection
    

        
    def send_message_end_effector_entering_button_area(self):
        """! The Computer_SendMessage_Rpi class initializer.
        @return  The Computer send a message to the Raspberri Pi that we are entering a button's area.
        """
        for button_area in self.parameter.list_buttons_area:
            if button_area.name == self.parameter.working_on_button and button_area.send_message_entering_area == True:
                ## send the socket message
                self.connection.send(str(button_area.time_end_effector_entering_area)+";"+ button_area.name +";" + "entering")
                button_area.send_message_entering_area = False
        pass
    
    def send_message_end_effector_leaving_button_area(self):
        """! The Computer_SendMessage_Rpi class initializer.
        @return  The Computer send a message to the Raspberri Pi that we are leaving a button's area.
        """
        for button_area in self.parameter.list_buttons_area:
            if button_area.name == self.parameter.working_on_button and button_area.send_message_leaving_area == True:
                ## send the socket message
                self.connection.send(str(button_area.time_end_effector_leaving_area)+";"+ button_area.name +";" + "leaving")
                button_area.send_message_leaving_area = False
   
    def run(self):
        """! Retrieves Computer_SendMessage_Rpi description.
        @return  A thread that runs during the RET.
        """
        while RET_config.stop_thread == False:
            self.send_message_end_effector_entering_button_area()
            self.send_message_end_effector_leaving_button_area()
            if RET_config.stop_thread == True:
                self.connection.send("STOP")
        self.connection.close()
        
    
class Computer_SocketClient_RET(RET_Parameter.RET_Parameter):
    """! The Computer_SocketClient_RET RET class.
    Provides a socket's client.
    """
    def __init__(self,parameter):
        """! The Computer_SendMessage_Rpi class initializer.
        @param parameter  The parameter we are working with.
        @return  Two thread that communicates from the computer to the Raspberri Pi.
        """
        self.parameter = parameter
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.connection.connect((parameter.socket_host, parameter.socket_port))
        except socket.error:
            print "Connection has failed."
            sys.exit()   
        print "Connection established with the servor."
        try:
            th_Computer_ReceiveMessage_Rpi = Computer_ReceiveMessage_Rpi(self.parameter,self.connection)
            th_Computer_ReceiveMessage_Rpi.start()
            th_Computer_SendMessage_Rpi = Computer_SendMessage_Rpi(self.parameter,self.connection)
            th_Computer_SendMessage_Rpi.start()
        except KeyboardInterrupt :
            RET_config.stop_thread = True

