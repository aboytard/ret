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
# - os : to kill the nodes

import rospy
import geometry_msgs.msg
from geometry_msgs.msg import PoseStamped
import os
from control_msgs.msg import JointTrajectoryControllerState


import RET_config

class Button_Masher_Application_node_listener():
    """! The Button_Masher_Application_node_listener base class.
    Defines the base class used by the RET to subscribe to the /tool_pose topic and get
    the end effector cartesian position.
    """
    def __init__(self):
        """! The Button_Masher_Application_node_listener base class initializer.
        """
        self.diagnostics_sub = rospy.Subscriber('tool_pose', PoseStamped, self.diagnostics_callback)
        ## add the listening of the joint position node see if it works
        self.diagnostics_additional = rospy.Subscriber('/prbt/manipulator_joint_trajectory_controller/state', JointTrajectoryControllerState, self.additional_callback)
        self.x = 0
        self.y = 0
        self.z = 0
    
    def diagnostics_callback(self, diagnostics):
        """! Retrieves the Button_Masher_Application_Output.
        @return  the affectation of the cartesian position of the end effector while the each time the node subscribe to the /tool_pose topic
        while node tool_pose_publisher_use is running.
        """
        self.x = diagnostics.pose.position.x
        self.y = diagnostics.pose.position.y
        self.z = diagnostics.pose.position.z
    
    def print_end_effector_position_information(self):
        """! Retrieves the Button_Masher_Application_Output.
        @return  the cartesian position of the end effector while the node tool_pose_publisher_use is running.
        """
        print ("End Effector x position is:", self.x)
        print ("End Effector y position is:", self.y)
        print ("End Effector z position is:", self.z)

    def additional_callback(self,diagnostics):
        self.actual_joint_state= diagnostics.actual.positions
        self.encoded_state=diagnostics.desired.positions
        self.error_state=diagnostics.error.positions
    
def launch_node_listener():
    """! Initialize the node tool_pose_publisher_use.
    @return the node tool_pose_publisher_use with a high frequency spin.
    @return when there is a key board interrupt, kill all the node running on the computer
    """
    while RET_config.stop_thread == False:
        rospy.init_node("RET_node", anonymous=False)
        rospy.spin()
    if RET_config.stop_thread == True:
        print("we are killing all nodes because we were asked to")
        nodes = os.popen("rosnode list").readlines()
        for i in range(len(nodes)):
            nodes[i] = nodes[i].replace("\n","")
        for node in nodes:
            os.system("rosnode kill "+ node)
#if __name__ == '__main__':
#    rospy.init_node("tool_pose_publisher_use", anonymous=True)
#    myInformer = Button_Masher_Application_node_listener()
#    rospy.spin()
    
