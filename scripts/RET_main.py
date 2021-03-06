#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 09:48:38 2021

@author: ret
"""

"""! @brief Define the RET."""
##
# @mainpage RET Project Alban
# @section description_main Description
# The application you run for the RET to communicate with the Rpi.
# The movement of the robot, the end effector cartesian position, the information about the button are the input of this function
# The output of the application is to know if the button are pressed inside an interval of time
# The interval of time is defined as the time the end effector enter and live the button's area
#
# @section notes_main Notes
#
# Copyright (c) 2021 Alban Boytard.  All rights reserved.

##
# @file RET_main.py
#
#@section libraries_RET_main Libraries/Modules
# Custom class in : RET_config, RET_Parameter, RET_socket, RET_data_processing

#@section todo_ret TODO
# - rosrun ret RET_main.py

# @section author_doxygen_example Author
# -Created by Alban Boytard on 25/01/2021


# Imports
import Button_Masher_Application_Output
import RET_Parameter
import RET_socket
import RET_config
import RET_data_processing

#Functions
def main(list_buttons_area):
    """! The main function.
    Launch all the thread and the node listening to ROS information.
    """    
    try:
        ##create listener of the Button Masher Application
        my_Button_Masher_Application_Output = Button_Masher_Application_Output.Button_Masher_Application_node_listener()
        ##create instance of parameter for the RET
        parameter = RET_Parameter.RET_Parameter(my_Button_Masher_Application_Output, list_buttons_area)
        ##create the node listener
        ##create the processing and data log
        th_Computer_data_processing = RET_data_processing.RET_data_processing(parameter)
#        th_Computer_data_processing.setDaemon(True)
        th_Computer_data_processing.start()
        ##create the socket communication
        socket_client = RET_socket.Computer_SocketClient_RET(parameter)
        #launch the subscribing node
        Button_Masher_Application_Output.launch_node_listener()
    except KeyboardInterrupt:
        RET_config.stop_thread = True




if __name__=="__main__":
    list_buttons_area = RET_config.list_buttons_area
    main(list_buttons_area)