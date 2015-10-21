# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 11:56:10 2015

@author: dimitris
"""

############ Import data from files and store to arrays/list ##################
import numpy as np
from lourandos import create_table
filename1 = 'main_faults_all.csv'
filename2 = 'Philippe_01_2007.csv'
#read and store the FAULTS csv as numpy array
row_count, fulltable = create_table(filename1)
fault_symptom = fulltable[1:row_count]
fault_symptom = [x[1:len(x)] for x in fulltable[1:row_count]]
fault_symptom = np.array([ map(float,x) for x in fault_symptom ])

# Store the engine's parameters(symptoms) in a list
parameters = fulltable[1:]
# Store the engine's possible faults in a list
faults = [fulltable[i][0] for i in range(1, row_count)]

# Other input parameters

error_margin = np.zeros(52)
error_margin[23]= 7 # Error margin for Texh 
error_margin[14]= 3 # Error margin for indicated Power 
error_margin[16]= 3 # Error margin for Pcomp 
error_margin[17]= 3 # Error margin for Pmax
error_margin[18]= 3 # Error margin for TC speed
error_margin[19]= 7 # Error margin for Pscav
error_margin[20]= 12 # Error margin for Tscav
error_margin[50]= 10 # Error margin for Pcomp/Pscav
error_margin[25]= 20 # Error margin for Pmax - Pcomp
error_margin[51]= 10 # Error margin for TC speed/Pscav
error_margin[15]= 3 # Error margin for Shaft Power
error_margin[22]= 7 # Error margin for Pexh
error_margin[21]= 25 # Error margin for Air Cooler Pressure Drop
#critical_indeces = [int(fulltable[i][-1]) for i in range(1, row_count)]

#read and store the MEASUREMENTS csv
#try: cases
#except NameError: cases = None

row_count2, fulltable2 = create_table(filename2)
#if cases is None:
#    pass
#else:
#    cases.insert(0,0)
#    fulltable2 = [fulltable2[i] for i in cases]
#    row_count2 = len(cases)
    
vessel_name = 'CAP PHILIPPE';

HC_data = fulltable2[1:row_count2]
HC_data = [x[1:len(x)] for x in HC_data]
HC_data = np.array(HC_data, dtype='str')
HC_data[HC_data =='']='0' # convert emtpy strings to zeros
HC_data= HC_data.astype('float')

# Add two last rows in HC_data
Tc_Pscav = HC_data[18]/HC_data[19]
Pcomp_Pscav = HC_data[16]/HC_data[19]
HC_data = np.row_stack(( HC_data, Tc_Pscav, Pcomp_Pscav ))

# Calculate differences and append to HC_data
ex = HC_data[:,0] 
obs = HC_data[:,1]
diff = obs-ex
diff_percent = diff/obs*100
fs = np.zeros(len(error_margin))

for i in range(len(error_margin)):   
    if np.isnan(diff_percent[i]) or diff_percent[i] == -inf:
        fs[i] = 100.
    else: 
        if diff_percent[i] > error_margin[i]:
            fs[i] = 1.
        elif diff_percent[i] < -error_margin[i]:
            fs[i] = -1.
        else:
            fs[i] = 0.
            
# Create the final numpy array (matrix), 52 x 5 cols 
HC_data = np.column_stack(( HC_data, diff, diff_percent, fs ))






