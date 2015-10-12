# -*- coding: utf-8 -*-
"""
Created on Thu Oct 01 11:33:04 2015
@author: dimitris lourandos
"""
###############################################################################
#------------------------FUNCTIONS USED---------------------------------------#
###############################################################################

# a try to use numpy arrays for operations to increase speed

import numpy as np
import matplotlib.pyplot as plt
#import matplotlib.dates as mdates
from lourandos import *

cases = range(240,245) # exclude zeros
lim_main  = 4
lim_suppl = 1 
filename1 = 'main_faults_some.csv'
filename2 = 'all_reports_input_new_2.csv'
na = '100' # number representing a symptom that is not available

###############################################################################
#-----------------------GETTING INITIAL DATA FROM FILES-----------------------#
###############################################################################

#read and store the FAULTS csv
row_count, fulltable = create_table(filename1)
fault_symptom = fulltable[1:row_count]
#fault_symptom = [x[1:len(x)] for x in fulltable[1:row_count]]
#fault_symptom = np.array([ map(float,x) for x in fault_symptom ])

#Sort fulltable by possibility (use possibilty column, no.9)
#fault_symptom.sort(reverse = True, key = lambda x: float(x[9]))

# Separate main and supplemetary parameters in 2 different lists (tables)
fault_symptom_main = [fault_symptom[i][0:10] for i in range(row_count-1)]
fault_symptom_suppl = [fault_symptom[i][10:len(fault_symptom[0])-1] for i in range(row_count-1)]

# Store the engine's parameters(symptoms) in a list
parameters = fulltable[0]
parameters_main = fulltable[0][1:9]
parameters_suppl = fulltable[0][10:]
# Store the engine's possible faults in a list
faults = [fulltable[i][0] for i in range(1, row_count)]
possibilities = [fulltable[i][9] for i in range(1, row_count)]
critical_indeces = [int(fulltable[i][-1]) for i in range(1, row_count)]
#read and store the MEASUREMENTS csv
try: cases
except NameError: cases = None

row_count2, fulltable2 = create_table(filename2)
if cases is None:
    pass
else:
    cases.insert(0,0)
    fulltable2 = [fulltable2[i] for i in cases]
    row_count2 = len(cases)
    
vessel_name = []; date = [];
meas_main = [0]*(row_count2-1); meas_suppl = [0]*(row_count2-1);
for i in range (1, row_count2):    
    vessel_name.append(fulltable2[i][0]) # Store vessel's name in a list
    date.append(fulltable2[i][1])        # Store the report date in a list
    meas_main[i-1] = fulltable2[i][2:10] # Store the main parameters of the measurements in a list
    meas_suppl[i-1] = fulltable2[i][11:len(fulltable2[i])+1] # Store the supplementary parameters of the measurements in a list

#(vessel_name, date) = map(list, zip(*[(fulltable2[i][0], fulltable2[i][1]) for i in range (1, row_count2)]))

###############################################################################
#-----------CHECK FOR ERRONEOUS MEASUREMENTS or FAULTY SENSORS----------------#
###############################################################################

#          MAIN PARAMETERS
# 0 = Exhaust Gas Temperature (Texh)
# 1 = Scavenge Pressure(Pscav)
# 2 = Turbocharger Speed (TC Speed)
# 3 = Pcomp/Pscav
# 4 = Maximum Pressure (Pmax)
# 5 = Compression Pressure (Pcomp)
# 6 = Brake Specific Fuel Consumption (BSFC)
# 7 = Pmax - Pcomp 

# Print symptoms
for i, meas in enumerate(meas_main):
    for j, symptom in enumerate(meas):
        check_meas(parameters_main[j], symptom)
    print



for i, meas in enumerate(meas_main):
    # 1. Pscav 
    if meas[1] !='0' and meas[3] !='0' and meas[5] == '0':  
        print '{}_Check Pscav measurement'.format(i)
#        cc[i] = 'Check Pscav measurement'
    # 2. BSFC
    if meas[6] =='-1' and all([I == '0' for n, I in enumerate(meas) if n!=6]):
        print '{}_Check Fuel Consumption or Power measurement'.format(i)
#        bc[i] = 'Low BSFC - Please check Fuel Consumption or Power measurement'
    if meas[6] == '1' and all([I == '0' for n, I in enumerate(meas) if n!=6]):
        print '{}_High BSFC - Please check Power or Fuel Consumption Measurement'.format(i)
    # 3. TDC Correction
    if meas[4] =='0' and meas[5] =='0' and meas_suppl[i][-1] !='0':
#        tdc[i] = 'Check TDC correction'
        print '{}_Check indicator diagram for TDC correction\
        or Torsion Meter measurement'.format(i) #i, tdc[i] 
    # 4. TC speed
    if meas[2] !='0' and all([I == '0' for n, I in enumerate(meas) if n!=2]):
        print "{}_Check Turbocharger Speed measurement".format(i)
#    # 5. Torsion Meter
#    if meas_suppl[i][20] != 0 and all([I == '0' for I in meas]):
#	print 'Please check Torsion Meter reading' 
    # 6. Pscav, Pexh - This has to be done on HC level (absolute numbers not 1's and 0's)
#    if meas[1] - meas_suppl[i][1] < 0:
#        print 'Exete metrisei malakies'
#    elif meas[1] - meas_suppl[i][1] < 0.1:
#        print 'Small Pscav - Pexh difference - Pls check both measurements' 
#    elif meas[1] - meas_suppl[i][1] > 0.4:
#        print 'Very large Pscav - Pexh difference - Pls check both measurements'         
#    print
    # 7. Exhaust gas temperature (it can be an indication of many faults
    #    even if it is present alone, without any other symptoms)
    if meas[0] == '-1' and all([I == '0' for I in meas]):
        print '{}_Check for faulty exhaust receiver temperature sensor'.format(i)
    elif meas[0] == '1' and all([I == '0' for I in meas]):
        print '{}_High exhaust gas temperature, check for:\
                i. Faulty exhaust receiver temperature sensor\
                ii. Inadequate fuel oil cleaning\
                iii. Altered combustion characteristics of fuel'.format(i)



