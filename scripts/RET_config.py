#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 15:40:24 2021

@author: ret
"""

class Btn():
    def __init__(self,name,x,y,z):
        self.name = name
        self.x = x
        self.y = y
        self.z = z
        pass
    
class Btn_area(Btn):
    def __init__(self,Btn,dx,dy,dz):
        self.name = Btn.name
        self.upper_x = Btn.x + dx
        self.upper_y = Btn.y + dy
        self.upper_z = Btn.z + dz
        self.lower_x = Btn.x - dx
        self.lower_y = Btn.y - dy
        self.lower_z = Btn.z - dz  
        self.end_effector_inside_area = False
        self.send_message_entering_area = False
        self.send_message_leaving_area = False
        pass
 
stop_thread = False    
delta_area = [0.06,0.0,0.05]    
Btn1 = Btn("Btn1",-0.1,-0.47,0.155)
Btn2 = Btn("Btn2",0.05,-0.47,0.155)

Btn1_area = Btn_area(Btn1, delta_area[0], delta_area[1], delta_area[2])
Btn2_area = Btn_area(Btn2, delta_area[0], delta_area[1], delta_area[2])

list_buttons_area = [Btn1_area,Btn2_area]