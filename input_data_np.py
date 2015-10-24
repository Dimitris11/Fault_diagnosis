# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 11:56:10 2015

@author: dimitris
"""

############ Import data from files and store to arrays/list ##################
# Constants = [μ, Dc, γAir, γG, Pmcr, Nmcr]
const = np.array([0.72, 0.73, 1.4, 1.36, 18660, 91], dtype = 'float')

from lourandos import create_table

#read and store the FAULTS csv as numpy array
row_count, fulltable = create_table(filename1)
fault_symptom = fulltable[1:row_count]
fault_symptom = [x[2:len(x)] for x in fulltable[1:row_count]]
fault_symptom = np.array([ map(float,x) for x in fault_symptom ])
cr = np.array( [ x[1] for x in fulltable[1:row_count] ], dtype = 'int' )
# Store the engine's parameters(symptoms) in a list
parameters = fulltable[1:]
# Store the engine's possible faults in a list
faults = [fulltable[i][0] for i in range(1, row_count)]

# Other input parameters


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
parameters_all = [x[0] for x in fulltable2[1:]]
HC_data = fulltable2[1:row_count2]
HC_data = [x[1:len(x)] for x in HC_data]
HC_data = np.array(HC_data, dtype='str')
HC_data[HC_data =='']='0' # convert emtpy strings to zeros
HC_data = HC_data.astype('float')

## Add last rows in HC_data

# Calculate Pcomp/Pscav, TCspeed/Pscav, Pscav-Pexh 
Pcomp_Pscav = HC_data[16]/HC_data[19]
Tc_Pscav = HC_data[18]/HC_data[19]
Pscav_Pexh = HC_data[19] - HC_data[22]
# Calculate compressor efficiency
Pc = (HC_data[19] + HC_data[21]/1000)/HC_data[2]
f1 = (const[2]-1.)/const[2]
eff_C = ( 3614400*(HC_data[4]+273.15)*(Pc**f1 -1)/
(const[0]*(np.pi*const[1]*HC_data[18])**2) ) /0.9
# Calculate turbocharger efficiency
Pt =( (HC_data[2] + HC_data[0] + (HC_data[48] + HC_data[49])/1000)/
HC_data[22] )
f2 = (const[3]-1.)/const[3]
eff_TC = ( 0.9055*(HC_data[4]+273.15)*(Pc**f1 -1)/
((HC_data[23]+273.15) * (1- Pt**(f2)) ) )
# Calculate the turbine efficiency
eff_T = eff_TC/eff_C

# Calculate engine Load
load_i = HC_data[15]/const[4]
HC_data = np.row_stack(( HC_data,Pcomp_Pscav, Tc_Pscav, Pscav_Pexh, eff_C, eff_T, eff_TC, load_i ))
parameters_all.extend(['Pcomp_Pscav', 'Tc_Pscav', 'Pscav_Pexh', 'eff_C', 'eff_T', 'eff_TC', 'Load'])

# Calculate differences and append to HC_data
ex = HC_data[:,0] 
obs = HC_data[:,1]
diff = obs-ex
diff_percent = diff/obs*100
error_margin = fs = np.zeros(len(HC_data))

error_margin[14]= 3 # Error margin for indicated Power 
error_margin[15]= 3 # Error margin for Shaft Power
error_margin[16]= 3 # Error margin for Pcomp 
error_margin[17]= 3 # Error margin for Pmax
error_margin[18]= 3 # Error margin for TC speed
error_margin[19]= 7 # Error margin for Pscav
error_margin[20]= 12 # Error margin for Tscav
error_margin[21]= 25 # Error margin for Air Cooler Pressure Drop
error_margin[22]= 7 # Error margin for Pexh
error_margin[23]= 7 # Error margin for Texh 
error_margin[25]= 20 # Error margin for Pmax - Pcomp
error_margin[80]= 10 # Error margin for Pcomp/Pscav
error_margin[81]= 10 # Error margin for TC speed/Pscav
error_margin[83]= 5  # Error margin for Compressor efficiency
error_margin[84]= 5  # Error margin for Turbine efficiency
error_margin[85]= 5  # Error margin for Turbocharger efficiency

for i in range(len(HC_data)):   
    if np.isnan(diff_percent[i]) or diff_percent[i] == -inf:
        fs[i] = 100.
    else: 
        if diff_percent[i] > error_margin[i]:
            fs[i] = 1.
        elif diff_percent[i] < -error_margin[i]:
            fs[i] = -1.
        else:
            fs[i] = 0.
            
# Create the final numpy array (matrix), 52 rows (parameters) x 5 cols 
HC_data = np.column_stack(( HC_data, diff, diff_percent, fs ))

HC_rows = int(np.shape(HC_data)[0])
HC_cols = int(np.shape(HC_data)[1])





