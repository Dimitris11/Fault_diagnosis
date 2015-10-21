# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 14:04:09 2015
@author: dimitris

Fault diagnosis for a single measurement using numpy arrays/matrices
"""

import numpy as np
#import matplotlib.pyplot as plt

#cases = range(240,245) # exclude zeros
limit  = 40.
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

# Create the array for comparison from the HC_data
fs_rows = int(np.shape(fault_symptom)[0])
fs_cols = int(np.shape(fault_symptom)[1])

measurement = np.ones(fs_cols)
measurement[0]  = HC_data[23, 4] # 01. Texh
measurement[1]  = HC_data[19, 4] # 02. Pscav
measurement[2]  = HC_data[18, 4] # 03. TC speed
measurement[3]  = HC_data[50, 4] # 04. Pcomp/Pscav
measurement[4]  = HC_data[17, 4] # 05. Pmax
measurement[5]  = HC_data[16, 4] # 06. Pcomp
measurement[6]  = HC_data[14, 4] # 07. Indicated Power
measurement[7]  = HC_data[25, 4] # 08. Pmax-Pcomp
measurement[8]  = HC_data[22, 4] # 09. Pexh
measurement[9]  = HC_data[20, 4] # 10. Tscav
measurement[10] = HC_data[15, 4] # 11. Shaft Power
measurement[11] = HC_data[51, 4] # 12. TC speed/ Pscav

# Check if the symptoms in measurement are above the limit for all
# the available faults in the fault-symptom matrix

for i in range(fs_rows):
    c = 0. # counter
    n100 = fs_cols # initial number of columns
    for j in range(fs_cols):
        if measurement[j] == fault_symptom[i,j]:
            c += 1 # if the symptom is detected the counter increases
        if fault_symptom[i,j] == 100:
            n100 -= 1 # if a symptom is not mapped then the denominator decreases
    ratio = c/n100 *100
    if ratio >= 40:
        print faults[i]
#    if c >= limit:
#        print faults[i]        
        







