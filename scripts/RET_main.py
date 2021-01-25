#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 09:48:38 2021

@author: ret
"""

import Button_Masher_Application_Output
import RET_Parameter
import RET_socket
import RET_config
import RET_data_processing

def main(list_buttons_area):
    ##create listener of the Button Masher Application
    my_Button_Masher_Application_Output = Button_Masher_Application_Output.Button_Masher_Application_node_listener()
    ##create instance of parameter for the RET
    parameter = RET_Parameter.RET_Parameter(my_Button_Masher_Application_Output, list_buttons_area)
    ##create the node listener
    ##create the processing and data log
    th_Computer_data_processing = RET_data_processing.RET_data_processing(parameter)
    th_Computer_data_processing.setDaemon(True)
    th_Computer_data_processing.start()
    ##create the socket communication
    socket_client = RET_socket.Computer_SocketClient_RET(parameter)
    #launch the subscribing node
    Button_Masher_Application_Output.launch_node_listener()
    pass




if __name__=="__main__":
    list_buttons_area = RET_config.list_buttons_area
    main(list_buttons_area)