#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 09:54:17 2021

@author: ret
"""
import rospy
import geometry_msgs.msg
from geometry_msgs.msg import PoseStamped

class Button_Masher_Application_node_listener():
    def __init__(self):
        self.diagnostics_sub = rospy.Subscriber('tool_pose', PoseStamped, self.diagnostics_callback)
        self.x = 0
        self.y = 0
        self.z = 0
    
    def diagnostics_callback(self, diagnostics):
        self.x = diagnostics.pose.position.x
        self.y = diagnostics.pose.position.y
        self.z = diagnostics.pose.position.z
    
    def print_end_effector_position_information(self):
        print ("End Effector x position is:", self.x)
        print ("End Effector y position is:", self.y)
        print ("End Effector z position is:", self.z)
    


if __name__ == '__main__':
    rospy.init_node("tool_pose_publisher_use", anonymous=True)
    myInformer = Button_Masher_Application_node_listener()
    rospy.spin()
    
def launch_node_listener():
    rospy.init_node("tool_pose_publisher_use", anonymous=True)
    rospy.spin()