# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 13:11:10 2015

@author: dimitris
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Oct 01 11:33:04 2015
@author: dimitris lourandos
"""
###############################################################################
#------------------------FUNCTIONS USED---------------------------------------#
###############################################################################

#import numpy as np
#import matplotlib.pyplot as plt
#import matplotlib.dates as mdates
from lourandos import *

#cases = range(140,145) # exclude zeros
lim_main  = 4
lim_suppl = 1 
filename1 = 'main_faults_all.csv'
filename2 = 'all_reports_input_test.csv'
na = '100' # number representing a symptom that is not available

###############################################################################
#-----------------------GETTING INITIAL DATA FROM FILES-----------------------#
###############################################################################

#read and store the FAULTS csv as numpy array
row_count, fulltable = create_table(filename1)
fault_symptom = fulltable[1:row_count]
#fault_symptom = [x[1:len(x)] for x in fulltable[1:row_count]]
#fault_symptom = np.array([ map(float,x) for x in fault_symptom ])

#Sort fulltable by possibility (use possibilty column, no.9)
#fault_symptom.sort(reverse = True, key = lambda x: float(x[9]))

# Separate main and supplemetary parameters in 2 different lists (tables)
fault_symptom_main = [fault_symptom[i][0:10] for i in range(row_count-1)]
fault_symptom_suppl = [fault_symptom[i][10:len(fault_symptom[0])] for i in range(row_count-1)]

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

execfile('sensors.py')