#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 12:16:16 2021

@author: ret
"""

import RET_Parameter
import socket,sys,threading
import RET_config
import datetime


class Computer_ReceiveMessage_Rpi(threading.Thread,RET_Parameter.RET_Parameter):
    def __init__(self,parameter,connection):
        threading.Thread.__init__(self)
        self.parameter = parameter
        self.connection = connection
    
    def run(self):
        while RET_config.stop_thread == False:
            received_message = self.connection.recv(1024)
            print "*" + received_message + "*"
            if received_message == "":
                print("We received a "" message so we stop the socket communication")
                break
            try:
                self.parameter.list_msg_Btn_Pressed = received_message.split(";")
                time_to_process = self.parameter.list_msg_Btn_Pressed[0]
                if self.parameter.list_msg_Btn_Pressed[2] == "pressed":
                    self.parameter.time_Btn_Pressed = datetime.datetime.strptime(time_to_process, '%Y-%m-%d %H:%M:%S.%f')
#                        print (self.parameter.time_Btn_Pressed)
#                        print(self.list_msg_Btn_Pressed)
#                        print(self.parameter.BtnMasherApplication_output.x)
            except:
                pass
        self.connection.close()


class Computer_SendMessage_Rpi(threading.Thread,RET_Parameter.RET_Parameter):
    def __init__(self,parameter,connection):
        threading.Thread.__init__(self)
        self.parameter = parameter
        self.list_msg_send = []
        self.connection = connection
    

        
    def send_message_end_effector_entering_button_area(self):
        for button_area in self.parameter.list_buttons_area:
            if button_area.name == self.parameter.working_on_button and button_area.send_message_entering_area == True:
                ## send the socket message
                self.connection.send(str(button_area.time_end_effector_entering_area)+";"+ button_area.name +";" + "entering")
                button_area.send_message_entering_area = False
        pass
    
    def send_message_end_effector_leaving_button_area(self):
        for button_area in self.parameter.list_buttons_area:
            if button_area.name == self.parameter.working_on_button and button_area.send_message_leaving_area == True:
                ## send the socket message
                self.connection.send(str(button_area.time_end_effector_leaving_area)+";"+ button_area.name +";" + "leaving")
                button_area.send_message_leaving_area = False
   
    def run(self):
        while RET_config.stop_thread == False:
            self.send_message_end_effector_entering_button_area()
            self.send_message_end_effector_leaving_button_area()
            pass         
    
class Computer_SocketClient_RET(RET_Parameter.RET_Parameter):
    def __init__(self,parameter):
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
            th_Computer_ReceiveMessage_Rpi._Thread__stop()
            th_Computer_SendMessage_Rpi._Thread__stop()
        

