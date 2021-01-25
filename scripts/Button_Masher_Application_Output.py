#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 09:54:17 2021

@author: ret
"""

# @file Button_Masher_Application_Output.py
#
# @brief Defines the Button Masher Application output as a class.
#
# @section Button_Masher_Application_Output Description
# Define one of the output of the Button Masher Application that we are using as an input for the RET:
# - the end effector cartesian position
#
# @section libraries_Button_Masher_Application_Output Libraries/Modules
# - rospy : enable to use python with ROS
# - geometry_msgs.msg.PoseStamped : define the type of message we want to listen when we subscribe a topic

import rospy
import geometry_msgs.msg
from geometry_msgs.msg import PoseStamped

class Button_Masher_Application_node_listener():
    """! The Button_Masher_Application_node_listener base class.
    Defines the base class utilized by the RET to subscribe to the /tool_pose topic and get
    the end effector cartesian position.
    """
    def __init__(self):
        """! The Button_Masher_Application_node_listener base class initializer.
        """
        self.diagnostics_sub = rospy.Subscriber('tool_pose', PoseStamped, self.diagnostics_callback)
        self.x = 0
        self.y = 0
        self.z = 0
    
    def diagnostics_callback(self, diagnostics):
        """! Retrieves the Button_Masher_Application_Output.
        @return  the cartesian position of the end effector while the node tool_pose_publisher_use is running.
        """
        self.x = diagnostics.pose.position.x
        self.y = diagnostics.pose.position.y
        self.z = diagnostics.pose.position.z
    
    def print_end_effector_position_information(self):
        print ("End Effector x position is:", self.x)
        print ("End Effector y position is:", self.y)
        print ("End Effector z position is:", self.z)
    
def launch_node_listener():
    """! Initialize the node tool_pose_publisher_use.
    @return the node tool_pose_publisher_use with a high frequency spin.
    """
    rospy.init_node("tool_pose_publisher_use", anonymous=True)
    rospy.spin()

#if __name__ == '__main__':
#    rospy.init_node("tool_pose_publisher_use", anonymous=True)
#    myInformer = Button_Masher_Application_node_listener()
#    rospy.spin()
    
