# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 11:56:10 2015

@author: dimitris
"""

############ Import data from files and store to arrays/list ##################
import numpy as np
from lourandos import create_table

#read and store the FAULTS csv as numpy array
row_count, fulltable = create_table(filename1)
fault_symptom = fulltable[1:row_count]
fault_symptom = [x[1:len(x)] for x in fulltable[1:row_count]]
fault_symptom = np.array([ map(float,x) for x in fault_symptom ])

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
    
vessel_name = 'CAP PHILIPPE';

HC_data = fulltable[1:row_count]
HC_data = [x[1:len(x)] for x in HC_data[1:row_count]]
HC_data = np.array([ map(float,x) for x in HC_data ])

for i in range (1, row_count2):    
    vessel_name.append(fulltable2[i][0]) # Store vessel's name in a list
    date.append(fulltable2[i][1])        # Store the report date in a list
    meas_main[i-1] = fulltable2[i][2:10] # Store the main parameters of the measurements in a list
    meas_suppl[i-1] = fulltable2[i][11:len(fulltable2[i])+1] # Store the supplementary parameters of the measurements in a list