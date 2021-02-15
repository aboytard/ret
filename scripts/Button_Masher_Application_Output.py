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
import datetime
from influxdb import InfluxDBClient

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
        self.diagnostics_sub = rospy.Subscriber('/prbt/manipulator_joint_trajectory_controller/state', JointTrajectoryControllerState, self.additional_callback)
        self.time_info = ""
        self.actual_state= ()
        self.encoded_state=()
        self.error_state=()
        self.cartesian_position_end_effector=""
        self.temperature=""
        self.voltage=""
        self.client = InfluxDBClient(host="localhost",port="8086",username='ret', password='asdf', database=RET_config.influxdb)
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


    def additional_callback(self, diagnostics):
        self.actual_state= diagnostics.actual.positions
        self.encoded_state=diagnostics.desired.positions
        self.error_state=diagnostics.error.positions
        self.write_into_db(self.client)
        self.data = self.write_info_json_into_db(self.client)
#        self.print_all_info()

    
    def print_all_info(self):
        print self.actual_state
        print self.encoded_state
        print self.error_state
        
    def write_into_db(self,client):
        client.create_database(RET_config.influxdb) ## Always writing in the same DB for now
#        print(client.get_list_database())   ## This will be useful to chose the name of the database for each test
        client.switch_database(RET_config.influxdb)
        
        
    def write_info_json_into_db(self,client):
        json_body_actual = [
            {
                "measurement": "actual_state",
                "tags": {
                    "requestName": "actual_state",
                    "requestType": "GET"
                },
                "time":datetime.datetime.utcnow(),
                 "fields": {
                    "prbt_joint1": self.actual_state[0],
                    "prbt_joint2": self.actual_state[1],
                    "prbt_joint3": self.actual_state[2],
                    "prbt_joint4": self.actual_state[3],
                    "prbt_joint5": self.actual_state[4],
                    "prbt_joint6": self.actual_state[5]
                            }
            }
        ]

        json_body_encoded = [
            {
                "measurement": "encoded_state",
                "tags": {
                    "requestName": "encoded_state",
                    "requestType": "GET"
                },
                "time":datetime.datetime.utcnow(),
                 "fields": {
                    "prbt_joint1": self.encoded_state[0],
                    "prbt_joint2": self.encoded_state[1],
                    "prbt_joint3": self.encoded_state[2],
                    "prbt_joint4": self.encoded_state[3],
                    "prbt_joint5": self.encoded_state[4],
                    "prbt_joint6": self.encoded_state[5]
                            }
            }
        ]
    
        json_body_error = [
            {
                "measurement": "error_state",
                "tags": {
                    "requestName": "error_state",
                    "requestType": "GET"
                },
                "time":datetime.datetime.utcnow(),
                 "fields": {
                    "prbt_joint1": self.error_state [0],
                    "prbt_joint2": self.error_state [1],
                    "prbt_joint3": self.error_state [2],
                    "prbt_joint4": self.error_state [3],
                    "prbt_joint5": self.error_state [4],
                    "prbt_joint6": self.error_state [5]
                            }
            }
        ]
   
        client.write_points(json_body_actual)
        client.write_points(json_body_encoded)
        client.write_points(json_body_error)
    
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
    
