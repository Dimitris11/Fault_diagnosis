# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 14:04:09 2015
@author: dimitris

Fault diagnosis for a single measurement using numpy arrays/matrices
"""

import numpy as np
from lourandos import check_meas2, check_meas_OK
#import matplotlib.pyplot as plt

#cases = range(240,245) # exclude zeros
limit     = 50. # Percentage ( % )
dominant  = 20. # Percentage ( % )
filename1 = 'Fault_Symptom_matrix.csv'
filename2 = 'Philippe_01_2007.csv'
#filename2 = 'CAP_THEODORA_06-2014.csv'

###############################################################################
#-----------------------GETTING INITIAL DATA FROM FILES-----------------------#
###############################################################################
print
execfile('input_data_np.py')
###############################################################################
#---------------------------PLOTTING OF BASIC DATA----------------------------#
###############################################################################

print 'SECTION 1 - Diagrams'
print
execfile('diagram_check.py')

###############################################################################
#-----------CHECK FOR ERRONEOUS MEASUREMENTS or FAULTY SENSORS----------------#
###############################################################################
print 'SECTION 2 - Differences observed'
print
j =4 # Column with -1, 0, 1
for i in [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 80, 81, 83, 84, 85]:
    check_meas2( parameters_all[i],HC_data[i,j-2], HC_data[i,j], units[i] )

print
print 'SECTION 3 - Sensor Faults:'
execfile('sensors_faults.py')

###############################################################################
#-------------------------MAIN BODY OF THE PROGRAM----------------------------#
###############################################################################


fs_rows = int(np.shape(fault_symptom)[0])
fs_cols = int(np.shape(fault_symptom)[1])

# Create the array for comparison from the HC_data
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
print 
print 'SECTION 4 - Main Algorithm:'
print
obs_faults = []
for i in range(fs_rows):
    ratio =0.
    c = 0. # counter
    n100 = fs_cols # initial number of columns
    for j in range(fs_cols):
        if measurement[j] == fault_symptom[i,j]:
            c += 1 # if the symptom is detected the counter increases
        if fault_symptom[i,j] == 100:
            n100 -= 1 # if a symptom is not mapped then the denominator decreases
        if measurement[cr[i]] == fault_symptom[i, cr[i]]:
            crOK = dominant
        else:
            crOK = 0.
#    print c, n100, crOK
    ratio = c/n100 *(100-dominant) + crOK
#    print c/n100*100, ratio
    if ratio >= limit:
        obs_faults.append([faults[i], ratio])
#        print faults[i]+ ' {:.2f}%'.format(ratio)
obs_faults.sort(reverse = True, key = lambda x: float(x[1]))
for i in obs_faults: print i[0], '{:.2f}'.format(i[1])+'%'
if obs_faults ==[]: print 'No faults detected from main algorithm'
print


print 'SECTION 5 - Components:'
print
execfile('Components.py')

print 'APPENDIX'
print
j=4
for i in [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 80, 81, 83, 84, 85]:
    check_meas_OK( parameters_all[i],HC_data[i,j-2], HC_data[i,j], units[i] )


#plt.close('all')