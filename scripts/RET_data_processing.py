#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 12:50:30 2021

@author: ret
"""

import RET_Parameter
import threading
import RET_config

class RET_data_processing(threading.Thread,RET_Parameter.RET_Parameter):
    def __init__(self,parameter):
        threading.Thread.__init__(self)
        self.parameter = parameter
        self.inside_one_button_area = False
        ## add a parameter that determine which button we have to work on, instead of working on every button of the list anytime
        self.button_area_workin_on = ""
        ## settle arguments to deal only with one Btn at the time, we cannot process every button of the list anytime
        pass
    
    def end_effector_inside_Btn_area(self):
        #return the time the end effector enter the button area
        try:
            if self.inside_one_button_area == False:
                for button_area in self.parameter.list_buttons_area :
                    if ((button_area.lower_x < self.parameter.BtnMasherApplication_output.x < button_area.upper_x ) and
                        (button_area.lower_y < self.parameter.BtnMasherApplication_output.y < button_area.upper_y ) and 
                        (button_area.lower_z < self.parameter.BtnMasherApplication_output.z < button_area.upper_z) and 
                        button_area.end_effector_inside_area == False):
                        button_area.end_effector_inside_area = True
                        self.inside_one_button_area = True
                        ### we determine the parameter that will tell the other one that it should only work on the button area the end effector was in previously
                        print ("we have enter the area of : ", button_area.name)
                self.inside_one_button_area = True
            if self.inside_one_button_area == True:
                for button_area in self.parameter.list_buttons_area :
                    if((button_area.lower_x > self.parameter.BtnMasherApplication_output.x or self.parameter.BtnMasherApplication_output.x > button_area.upper_x ) or
                       (button_area.lower_y < self.parameter.BtnMasherApplication_output.y or self.parameter.BtnMasherApplication_output.y > button_area.upper_y ) and 
                       (button_area.lower_z < self.parameter.BtnMasherApplication_output.z or self.parameter.BtnMasherApplication_output.z> button_area.upper_z) and 
                       button_area.end_effector_inside_area == True):
                        button_area.end_effector_inside_area = False
                        print ("we have left the area of : ", button_area.name)
                self.inside_one_button_area = False
        except:
            print("probleme dans la compilation")


 

    
    def process_time_Btn_pressed(self):
        ## process the time of the button is pressed with the time the button enter and leave the button area
        pass
    
    def run(self):
        while RET_config.stop_thread == False:
           self.end_effector_inside_Btn_area()
        pass