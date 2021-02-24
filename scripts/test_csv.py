#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 16:45:50 2021

@author: ret
"""

import csv
import datetime
list_coco = ["caca","coco",True,["a",datetime.datetime.utcnow()]]
date = datetime.datetime.utcnow()
list_coco.append(str(date))
coco = "test.csv"
with open('./RET_csv_logfile/'+"Btn1_Btn2_[[-0.1, -0.41, 0.145], [0.05, -0.41, 0.145]][0.06;0.06;0.013_acceleration_factor_[3.49]_velocity_factor_[1.57]_robot_settle_time_[0.2]_native.csv","aw") as f:
    cr = csv.writer(f,delimiter=",",lineterminator="\n")
    cr.writerow(list_coco)
print list_coco