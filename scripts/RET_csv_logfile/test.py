#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 16:51:16 2021

@author: ret
"""

import csv

with open('/home/ret/workspaces/ret/src/ret/scripts/RET_csv_logfile/RET_TestBtn1_Btn2_[[-0.1, -0.47, 0.153], [0.05, -0.47, 0.153]][0.06;0.05;0.02]_bouncetime_[200, 200]_acceleration_factor_[1.7]_velocity_factor_[1.57]_robot_settle_time_0.01]_ROS.csv',"w") as f:
    cr = csv.writer(f,delimiter=";",lineterminator="\n")
    cr.writerow(['datetime.utcnow','Btn_name','Action','In_Time_Interval'])
