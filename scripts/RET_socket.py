#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 12:16:16 2021

@author: ret
"""

import RET_Parameter
import socket,sys,threading
import RET_config


class Computer_ReceiveMessage_Rpi(threading.Thread,RET_Parameter.RET_Parameter):
    def __init__(self,parameter,connection):
        threading.Thread.__init__(self)
        self.parameter = parameter
        self.connection = connection
    
    def run(self):
        while RET_config.stop_thread == False:
            received_message = self.connection.recv(1024)
            print "*" + received_message + "*"
            try:
                self.list_msg_Btn_Pressed = received_message.split(";")
                for i in self.parameter.list_buttons_area:
                    if self.list_msg_Btn_Pressed[1] == i.name:
                        self.parameter.time_Btn_Pressed = self.list_msg_Btn_Pressed
                        print (self.parameter.time_Btn_Pressed)
                        print(self.list_msg_Btn_Pressed)
                        print(self.parameter.BtnMasherApplication_output.x)
            except:
                pass


class Computer_SendMessage_Rpi(threading.Thread,RET_Parameter.RET_Parameter):
    def __init__(self,parameter):
        threading.Thread.__init__(self)
        self.parameter = parameter
    
    def run(self):
        while RET_config.stop_thread == False:
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
        except KeyboardInterrupt :
            th_Computer_ReceiveMessage_Rpi._Thread__stop()
        

