# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 14:04:09 2015
@author: dimitris

Fault diagnosis for a single measurement using numpy arrays/matrices
"""

import numpy as np
#import matplotlib.pyplot as plt

#cases = range(240,245) # exclude zeros
limit  = 4
filename1 = 'main_faults_all.csv'
filename2 = 'Philippe_01_2007.csv'

###############################################################################
#-----------------------GETTING INITIAL DATA FROM FILES-----------------------#
###############################################################################

execfile('input_data_np.py')

###############################################################################
#-----------CHECK FOR ERRONEOUS MEASUREMENTS or FAULTY SENSORS----------------#
###############################################################################

execfile('sensors.py')

###############################################################################
#-------------------------MAIN BODY OF THE PROGRAM----------------------------#
###############################################################################

# 1st part - Compare Main Symptoms
i=-1; bc = ['']*len(vessel_name); cc = ['']*len(vessel_name);
tdc = ['']*len(vessel_name); c_save = ['']*len(faults);
c2_save = [];
main_faults = ['0']*len(meas_main)
fault_counter = ['0']*len(meas_main)

for meas in meas_main: # check every case (report, measurement) -> meas = list
    i +=1
    main_faults_in = list(); fault_counter_in = list()
    c_save = ['']*len(faults)
    for fault_i in range(len(fault_symptom_main)):
        c = 0 #counter 
        for symptom_i in range(1, len(fault_symptom_main[fault_i])-1):
#            print symptom_i
            if meas[symptom_i-1] == fault_symptom_main[fault_i][symptom_i] or\
            meas[symptom_i-1] == na:
                c += 1
        if c >= lim_main:
            main_faults_in.append(fault_symptom_main[fault_i])
            fault_counter_in.append(fault_i)
        c_save[fault_i] = int(c)
    c2_save.append(c_save)
#   print c_save
    main_faults[i] = main_faults_in # this needs to be revisited
    fault_counter[i] = fault_counter_in # this provides right results