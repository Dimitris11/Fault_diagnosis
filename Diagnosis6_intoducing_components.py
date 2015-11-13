# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 15:19:04 2015

@author: dimitris
"""

ff_all =[]; sensor_warning = []
#vessel_name = 'CAP PHILIPPE';
#loading   = 0 # 1 if vessel is loaded, 0 if in ballast condition
limit     = 20. # Percentage ( % )
dominant  = 25. # Percentage ( % )
filename1 = 'Fault_Symptom_matrix_component.csv'
filename2 = 'Philippe_01_2007_enhanced.csv'
#filename2 = 'ADP_AUG_CAP FELIX_2014_unprotected_celsius.CSV'
#filename2 = 'ADP_JUN_CAP CHARLES_2014 - unprotected_Shaft.CSV'
#filename2 = 'ADP_NOV_CAP VICTOR_2014 - UNPROTECTED.CSV' # loading = 0
#filename2 = 'ADP_OCT_CAP GUILLAUME_2014_unprotected_celsius.CSV'

###############################################################################
#------------------------ FUNCTIONS USED IN PROGRAM --------------------------#
###############################################################################
from math import pi

def linear_interpolation(x, x_list, y_list):
    """ 
    Takes as arguments the x coordinate at which we want to interoplate
    and two lists x,y that define the points of the function.
    """
    # Turn all numbers to floats
    x = float(x) 
    x_list = map(float, x_list)
    y_list = map(float, y_list)
    
    if x >= x_list[0] and x <= x_list[-1]:
        if x in x_list:
            idx = x_list.index(x)
            y = y_list[idx]
            return y
        for i in range(len(x_list)-1):
            if (x-x_list[i])*(x-(x_list[i+1])) < 0:
                x0 = x_list[i]
                x1 = x_list[i+1]
                y0 = y_list[i]
                y1 = y_list[i+1]
                a = (y1-y0)/(x1-x0)
                y = y0 + a*(x-x0)
                return y
    else:
        return 'X parameter out of limits'

def create_table(filename):
    ''' This function takes a file path as input and returns 
    the number of file rows and a matrix with the data included in the file'''
    import csv    
    out = open(filename, 'r')
    data = csv.reader(out, delimiter=';')
    fulltable = [row for row in data]
    # count the rows
    row_count = sum(1 for row in fulltable)
    out.close()
    #print row_count
    return row_count, fulltable


###############################################################################
#----------------------DATA FROM SHOP/SEA FOR CORRELATIONS--------------------#
###############################################################################

### Constants = [μ, Dc, γAir, γG, Pmcr, Nmcr, TC mechanical efficiency]
const = map(float, [0.72, 0.73, 1.4, 1.36, 18660, 91, 0.9])

rpm_min = 50.0; rpm_MCR = 91.0; rpm_max = 93.9
power_min =  2500.; power_max = 20000.

### Data from SHOP TEST
Load = [x/100. for x in [25, 50, 75, 90, 100, 110]]
rpm_shop = map(float,[ 57.4, 72.3, 82.6, 87.9, 91,	93.9 ])
power_shop = map(float,[ 4313, 8475, 12761, 15376, 17121, 18732 ])
eff_mech_shop = map(float,[0.871346791, 0.913658654, 0.933402422, \
0.940307356, 0.944465013, 0.944609484])
Pscav_shop = map(float,[1.38058, 2.13032, 2.93965, 3.43898, 3.80898, 4.06898])
pscav_pexh_shop = [0.07, 0.15, 0.20, 0.29, 0.28, 0.24]
backpressure_shop = map(float,[0, 3.92266, 7.84532, 14.709975, 15.69064, 22.555295]) # mbar
AF_shop = map(float,[0.000490333, 0.001372931, 0.002745862,	0.003285228, 0.00392266, 0.004511059])

### Data from SEA TRIALS
# Corrected FPI for Sea Trials simulation with ThermoS
FPI_sea = map(float,[72.33, 75.33, 80, 84.17, 85.33, 88.17])
# Indicated Power from sea trials simulation with ThermoS
power_ind_sea_sim = map(float,[13425.5, 14014, 15870, 16695, 17517.4, 18042])
egb_drop = 5 # mbar

### Data from both SHOP/SEA
rpm_trials = map(float,[57.4, 72.3, 82.6, 87.9	, 91, 93.9, 85.9,	85.9, 90.9,\
90.69, 94.09])
DTww_shop = map(float,[1.5, 5.5, 13, 16.5, 21.5, 25.5])

###############################################################################
#-----------------------GETTING INITIAL DATA FROM FILES-----------------------#
###############################################################################
#print
############ Import data from files and store to arrays/list ##################

#read and store the FAULTS csv as numpy array
row_count, fulltable = create_table(filename1)
fault_symptom = fulltable[1:row_count]
#fulltable = [['Faults', 'critical param', 'Exhaust Gas Temp', 'Scavenge Pressure', 'Turbocharger Speed', 'Pcomp/Pscav', 'Maximum Pressure', 'Compression Pressure', 'Indicated Power', 'Pmax-Pcomp', 'Pexh', 'Tscav', 'Shaft Power', 'TC speed/Pscav'],
#['Injection nozzles (or fuel valves) in poor condition, nozzle tip broken', '4', '1', '1', '1', '1', '-1', '1', '0', '-1', '1', '1', '0', '1'],
#['Start of injection too late', '4', '1', '1', '1', '0', '-1', '1', '100', '-1', '1', '0', '100', '0'],
#['Turbine Rotor blade tips damaged (rubbing)', '2', '1', '-1', '-1', '0', '-1', '-1', '100', '1', '-1', '0', '100', '-1'],
#['Exhaust valve leaking', '5', '1', '1', '1', '-1', '-1', '-1', '-1', '100', '100', '1', '-1', '100'],
#['Blow-by in combustion chamber', '5', '1', '1', '1', '-1', '-1', '-1', '-1', '1', '1', '1', '-1', '-1'],
#['Air Filter before Compressor fouled', '0', '1', '-1', '1', '0', '-1', '-1', '100', '0', '-1', '0', '100', '1'],
#['Fouled air or water side (AC) -Cooling water pipes or water passages chocked', '9', '1', '1', '1', '-1', '1', '1', '-1', '-1', '1', '1', '100', '-1'],
#['Start of injection too early', '4', '-1', '-1', '-1', '0', '1', '-1', '100', '1', '-1', '0', '100', '0']]
#row_count = len(fulltable)
fault_symptom = [x[2:len(x)] for x in fulltable[1:row_count]]
fault_symptom = [ map(float,x) for x in fault_symptom ]
# Critical parameter Indices
cr = map(int, [ x[1] for x in fulltable[1:row_count] ])
# Store the engine's parameters(symptoms) in a list
parameters = fulltable[0][2:]
# Store the engine's possible faults in a list
faults = [fulltable[i][0] for i in range(1, row_count)]
#for i in range(len(fault_symptom)):
#    fault_symptom[i].pop(10)
#    fault_symptom[i].pop(6)

fault_symptom_cyl = [fault_symptom[0]]+[fault_symptom[1]]+[fault_symptom[3]]\
+[fault_symptom[4]]+[fault_symptom[7]]

fault_symptom_TC = [fault_symptom[2]]+[fault_symptom[6]]
faults_cyl = faults[0:2]+faults[3:5]+[faults[7]]
faults_TC = [faults[2]]+[faults[6]]
#read and store the MEASUREMENT csv 
row_count2, fulltable2 = create_table(filename2)
parameters_all = [x[0] for x in fulltable2[1:]]
HC_data1 = fulltable2[1:row_count2]
HC_data = [x[1:3] for x in HC_data1]
#HC_data = map(str, HC_data)
#HC_data[HC_data =='']='0' # convert emtpy strings to zeros
for i, h in enumerate(HC_data):
    for j, h2 in enumerate(h):
        if h2 == '':
            HC_data [i][j] = '0'
HC_data = [map(float, i) for i in HC_data]
rpm = HC_data[1][1]


## Add last rows in HC_data

# Initialize empty lists(value = 0)
Pcomp_Pscav = [0]*len(HC_data[0])
Tc_Pscav = [0]*len(HC_data[0])
Pscav_Pexh = [0]*len(HC_data[0])
Pc = [0]*len(HC_data[0])
Pt = [0]*len(HC_data[0])
eff_C = [0]*len(HC_data[0])
eff_T = [0]*len(HC_data[0])
eff_TC = [0]*len(HC_data[0])
eff_m = [0]*len(HC_data[0])
load_i = [0]*len(HC_data[0])
# Calculate superscripts for TC efficiencies 
f1 = (const[2]-1.)/const[2]
f2 = (const[3]-1.)/const[3]

# Correlate the backpressure and EGB pressure drop from shop test 
# if these values are not recorded in the report

if HC_data[48][1] == 0: # Backpressure is not recorded
    backpressure = linear_interpolation(rpm, rpm_shop, backpressure_shop)
    HC_data[48][0] = HC_data[48][1] = backpressure
if HC_data[49][1] == 0:
    HC_data[49][1] = HC_data[49][0] = egb_drop

for i in range(len(HC_data[0])):
    
    # Calculate Pcomp/Pscav, TCspeed/Pscav, Pscav-Pexh 
    Pcomp_Pscav[i] = HC_data[16][i]/HC_data[19][i]
    Tc_Pscav[i] = HC_data[18][i]/HC_data[19][i]
    Pscav_Pexh[i] = HC_data[19][i] - HC_data[22][i]

    # Calculate compressor efficiency
    Pc[i] = (HC_data[19][i] + HC_data[21][i]/1000.)/HC_data[2][i]
    eff_C[i] = (3614400 *(HC_data[4][i] + 273.15) * (Pc[i]**f1 -1)/
    (const[0]*(pi*const[1] * HC_data[18][i])**2) ) / const[6]

    # Calculate turbocharger efficiency

    Pt[i] =( (HC_data[2][i] + HC_data[0][i] + (HC_data[48][i] + HC_data[49][i])/1000.)/ HC_data[22][i] )

    eff_TC[i] = ( 0.9055 *(HC_data[4][i] + 273.15) * (Pc[i]**f1 -1)/
    ( (HC_data[23][i]+273.15) * (1- Pt[i]**(f2)) ) )

    # Calculate the turbine efficiency
    eff_T[i] = eff_TC[i] /eff_C[i]

    # Calculate engine Load
    load_i[i] = HC_data[15][i]/const[4]

    # Calculate Mechanical Efficiency
    eff_m[i] = HC_data[15][i]/HC_data[14][i]
    
    
HC_data.extend([Pcomp_Pscav, Tc_Pscav, Pscav_Pexh, eff_C, eff_T, eff_TC, load_i, eff_m])
parameters_all.extend(['Pcomp_Pscav', 'Tc_Pscav', 'Pscav_Pexh', 'eff_C',\
'eff_T', 'eff_TC', 'Load', 'Mechanical efficiency'])

# Calculate differences and append to HC_data
ex   = [x[0] for x in HC_data] 
obs  = [x[1] for x in HC_data]
diff = [ (obs[i]-ex[i]) for i in range(len(HC_data)) ]
diff_percent = [0]*len(HC_data) # Initialize a list of zeros
diff_percent = [ (diff[i]/obs[i]*100.) if obs[i] !=0. else None for i in range(len(HC_data)) ]


# Manipulate per Component data
components = [ x[3:] for x in HC_data1 if x[3] !='' ]
for i, h in enumerate(components):
    for j, h2 in enumerate(h):
        if h2 == '':
            components [i][j] = '0'
components = [map(float, i) for i in components]

# Make components = -1, 0, 1
   

Pcomp_Pscav_component = [x/obs[19] for x in components[0]]
Pmax_Pcomp_component = [a - b for a, b in zip(components[1], components[0])]
Tc_Pscav_component = [x/obs[19] for x in components[2] if x!=0]
components.pop(3)
components.insert(2, Pcomp_Pscav_component)
components.insert(3, Pmax_Pcomp_component)
components.insert(4, [obs[23]])
components.insert(6, Tc_Pscav_component)
components.insert(7, [obs[19]])
components.insert(8, [obs[22]])
components.insert(9, [obs[20]])



cd = len(components)*[[]]
cd[0] = [(x-ex[16])/x for x in components[0] if x!=0]
cd[1] = [(x-ex[17])/x for x in components[1] if x!=0]
cd[2] = [(x-ex[80])/x for x in components[2] if x!=0]
cd[3] = [(x-ex[25])/x for x in components[3] if x!=0]
cd[5] = [(x-ex[18])/x for x in components[5] if x!=0]
cd[6] = [(x-ex[81])/x for x in components[6] if x!=0] 



error_margin = len(HC_data)*[0] # Initialize deviation for each parameter
error_margin[14]= 3  # Error margin for Indicated Power 
error_margin[15]= 3  # Error margin for Shaft Power
error_margin[16]= 3  # Error margin for Pcomp 
error_margin[17]= 3  # Error margin for Pmax
error_margin[18]= 3  # Error margin for TC speed
error_margin[19]= 7  # Error margin for Pscav
error_margin[20]= 12 # Error margin for Tscav
error_margin[21]= 25 # Error margin for Air Cooler Pressure Drop
error_margin[22]= 7  # Error margin for Pexh
error_margin[23]= 7  # Error margin for Texh 
error_margin[25]= 20 # Error margin for Pmax - Pcomp
error_margin[54]= 3  # Error margin for Shaft Power (Torsion meter)
error_margin[80]= 7  # Error margin for Pcomp/Pscav
error_margin[81]= 10 # Error margin for TC speed/Pscav
error_margin[83]= 5  # Error margin for Compressor efficiency
error_margin[84]= 5  # Error margin for Turbine efficiency
error_margin[85]= 5  # Error margin for Turbocharger efficiency
error_margin[87]= 3  # Error margin for engine mechanical efficiency




fs = len(HC_data)*[0] # Initialize an array of zeros to store the -1, 0, 1 
units = []
for i in range(len(HC_data)):   
    if diff_percent[i] == None :
        fs[i] = 100.
    else: 
        if diff_percent[i] > error_margin[i]:
            fs[i] = 1.
        elif diff_percent[i] < -error_margin[i]:
            fs[i] = -1.
        else:
            fs[i] = 0.
    s = parameters_all[i]
    if '[' in s: units.append(s[s.find("[")+1:s.find("]")])
    else: units.append(' ')   
            
component_data = len(components)*[[]]
component_data[0] = [1. if  x > error_margin[16]/100. else -1. if x < -error_margin[16]/100. else 0. for x in cd[0]]
component_data[1] = [1. if  x > error_margin[17]/100. else -1. if x < -error_margin[17]/100. else 0. for x in cd[1]]
component_data[2] = [1. if  x > error_margin[80]/100. else -1. if x < -error_margin[80]/100. else 0. for x in cd[2]]
component_data[3] = [1. if  x > error_margin[25]/100. else -1. if x < -error_margin[25]/100. else 0. for x in cd[3]]
component_data[4] = [fs[23]]
component_data[5] = [1. if  x > error_margin[18]/100. else -1. if x < -error_margin[18]/100. else 0. for x in cd[5]]
component_data[6] = [1. if  x > error_margin[81]/100. else -1. if x < -error_margin[81]/100. else 0. for x in cd[6]]
component_data[7] = [fs[19]]
component_data[8] = [fs[22]]
component_data[9] = [fs[20]]

#HC_rows = int(np.shape(HC_data)[0])
#HC_cols = int(np.shape(HC_data)[1])

###############################################################################
#-----------CHECK FOR ERRONEOUS MEASUREMENTS or FAULTY SENSORS----------------#
###############################################################################
#print 'SECTION 2 - Differences observed'
#print
observ_list = [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 80, 81, 83, 84, 85]
observations = []
for i in observ_list:
    if int(fs[i]) == -1:
        message = '{} is lower than expected'.format(parameters_all[i])
    elif int(fs[i]) == 1:
        message = '{} is higher than expected'.format(parameters_all[i])
    elif int(fs[i]) == 100:
        message = '{} not measured'.format(arameters_all[i])
    else:
        message = '0'
    observations.append(message)
observations = [x for x in observations if x !='0']
#print
#print 'SECTION 2 - Sensor Faults:'

#          MAIN PARAMETERS

# 23 = Exhaust Gas Temperature (Texh)
# 19 = Scavenge Pressure(Pscav)
# 18 = Turbocharger Speed (TC Speed)
# 50 = Pcomp/Pscav
# 17 = Maximum Pressure (Pmax)
# 16 = Compression Pressure (Pcomp)
# 12 = Brake Specific Fuel Consumption (BSFC)
# 25 = Pmax - Pcomp
# 14 = Indicated Power
# 15 = Shaft Power
# 80 = Pcomp/Pscav
# 81 = TC speed/Pscav
# 82 = Pscav - Pexh

# Print symptoms
k = 0 # Sensor Faults counter   
# Check for sensor faults/inconsistencies in measurements
#print
#print 'Now the sensor check starts:' 


# 1. Pscav 
if fs[19] !=0 and fs[16] ==0:
    ss = 'a. Check Scavenge Pressure measurement\
    b. Check Exhaust valve timing because of #1'
    k +=1; sensor_warning.append(ss)
    
# 2. BSFC
if (fs[12] !=0 and fs[17] ==0 and fs[23] ==0 and\
fs[18] ==0 and fs[14]) ==0:
    ss = 'Check Fuel Consumption or Power measurement because of #2'
    k +=1; sensor_warning.append(ss)
    
# 3. TDC Correction
if fs[17] ==0 and fs[16] ==0 and fs[14] !=0:
    ss = 'a.Check pressure diagram measurement\
    b. TDC correction procedure because of #3'
    k +=1; sensor_warning.append(ss)
    
# 4. TC speed
if fs[18] !=0 and fs[23] ==0 and fs[19] ==0 and \
fs[17] ==0 and fs[14] ==0:
    ss = "Check Turbocharger Speed measurement because of #4"
    k +=1; sensor_warning.append(ss)
    
# 5. Torsion Meter
if fs[15] !=0 and fs[23] ==0 and fs[19] ==0 and \
fs[17] ==0 and fs[16] ==0 and fs[14] ==0:
    ss = 'Please check Torsion Meter reading because of #5'
    k +=1; sensor_warning.append(ss)
    
# 6. Exhaust Gas Temperature     
if fs[23] !=0 and fs[17] ==0 and fs[18] ==0 and \
fs[14] ==0:
    ss = 'Check for faulty exhaust receiver temperature\
    sensor because of #6'
    k +=1; sensor_warning.append(ss)
    
#7. Texhaust & TC speed
if fs[23] ==1 and fs[18] ==-1:
    ss = 'Check for faulty exhaust receiver temperature sensor\
    and turbocharger speed measurement because if #7'
    k +=1; sensor_warning.append(ss)
if fs[23] ==-1 and fs[18] ==1:
    ss = 'Check for faulty exhaust receiver temperature sensor\
    and turbocharger speed measurement because if #7'
    k +=1; sensor_warning.append(ss)
    
#8. Scavenge pressure and TC speed
if fs[19] ==-1 and fs[18] == 1:
    ss = 'Check scavenge pressure because of #8'
    k +=1; sensor_warning.append(ss)
if fs[19] == 1 and fs[18] ==-1:
    ss = 'Check scavenge pressure because of #8'
    k +=1; sensor_warning.append(ss)   
    
#9. Pscav - Pexh  

pscav_pexh = linear_interpolation( rpm, rpm_shop, pscav_pexh_shop )

if HC_data[82][1] < 0.0:
    ss = "Exhaust receiver pressure is higher than scavenge receiver pressure:\
    Check both measurements!"
    k +=1; sensor_warning.append(ss)
elif HC_data[82][1] == 0.0:
    ss = "Exhaust receiver pressure and scavenge receiver pressure are the same:\
    Check both measurements!"
    k +=1; sensor_warning.append(ss)
elif HC_data[82][1] < 0.1:
    ss = "Check scavenge pressure or exhaust receiver pressure because their difference is small"
    k +=1; sensor_warning.append(ss)
elif HC_data[82][1] > 0.3:
    ss = "Check scavenge pressure or exhaust receiver pressure because their difference is large"
    k +=1; sensor_warning.append(ss)
elif HC_data[82][1] > pscav_pexh +0.1:
    ss = "Check scavenge pressure or exhaust receiver pressure because of #9b"
    k +=1; sensor_warning.append(ss)
elif HC_data[82][1] < pscav_pexh -0.1:
    ss = "Check scavenge pressure or exhaust receiver pressure because of #9b"
    k +=1; sensor_warning.append(ss)
    
#10. Compressor Efficiency
if HC_data[83][1] > 0.9:
    ss = "Check for high Pscav or low TC speed measurements because\
    compressor isentropic efficiency is {:.2f} when it\
    should be < 0.90".format(fs[83][1])
if HC_data[83][1] < 0.75:
    ss = "Check for low Pscav or high TC speed measurements because\
    compressor isentropic efficiency is {:.2f} when it\
    should be > 0.75".format(fs[83][1])
    k +=1; sensor_warning.append(ss)

#11. Shaft (FPI) vs Shaft from Torsion meter
if abs((HC_data[54][1] - HC_data[15][0])/HC_data[54][1] *100.) < 2:
    fs[54] = 0. # Shaft power is OK
else:
    ss = 'Check Torsion meter or FPI measurement'
    k +=1; sensor_warning.append(ss)

#12. Mechanical Efficiency
eff_m = HC_data[54][1]/HC_data[14][1]
if eff_m > 0.98:
    k +=1
    if fs[54] == 0:
        ss = 'Check Indicated Power measurement (low), very high mechanical efficiency'
    else: 
        ss = 'Check both Torsion meter and Indicated Power measurement, efficiency > 0.98'
elif eff_m < 0.85:
    k +=1
    if fs[54] == 0:
        ss = 'Check Indicated Power measurement (high), very low mechanical efficiency'
    else:
        ss = 'Check both Torsion meter and Indicated Power measurement, efficiency < 0.85'
sensor_warning.append(ss)
    
#12. Turbocharger Efficiency


print        
###############################################################################
#-------------------------------COMPONENTS------------------------------------#
###############################################################################	
#print 'SECTION 3 - Components:'
print	

### 1. AIR FILTER
#print '1. Air Filter'
# Step 1 - Build the Correlation from Shop Test
# Step 2 - Interpolate Shop Test data and find the expected pressure drop
AF_exp = linear_interpolation(HC_data[19][1], Pscav_shop, AF_shop )

AF_obs = HC_data[0][1]
# Step 3 - Compare observed and expected value and display message
AF_diff = (AF_obs - AF_exp)/AF_obs 
if AF_diff >= 0.4:
    ff = 'Air Filter is fouled and needs to be cleaned'
    ff_all.append(ff)
elif AF_diff < -0.1:
    ss = 'Air Filter pressure drop is less than normal - check measurement'
    k +=1; sensor_warning.append(ss)
#else:
#    print 'Air Filter is OK'
#print  

### 2. Air Cooler
#print '2. Air Cooler'
# Step 1 - Check Pressure Drop
if fs[21] ==  1:
    ff = 'a.The Air Cooler is fouled at the air side'
    ff_all.append(ff)
#elif fs[21,4] == 0:
#    print 'a.The Air Cooler\'s pressure drop is OK'
elif fs[21] == -1:
    if fs[18] == -1.0:
        ff = 'a.Possible reduction of air flow rate through Air Cooler'
        ff_all.append(ff)
    else:
        ss = 'a.Check Air Cooler pressure drop measurement'
        k +=1; sensor_warning.append(ss)
        
# Step 2 - Calculate and check effectiveness (high on low loads, lower on higher)
eff_AC = (HC_data[24][1]-HC_data[43][1])/(HC_data[24][1]-HC_data[5][1])
# limit, should be < 0.85
if eff_AC < 0.88:
    ff = 'b.Air Cooler Effectiveness is lower than expected. Possible fouling of AC or error in measurements'
    ff_all.append(ff)
elif eff_AC >= 0.98:
    ss = 'b.Air Cooler Effectiveness is high, check Air Cooler Delivery Temperature'
    k +=1; sensor_warning.append(ss)
#else:
#    print 'b.Air Cooler Effectiveness is OK'

# Step 3 - Calculate DTww and correlate with data from shop/sea trials
DTww_exp = linear_interpolation(rpm, rpm_shop, DTww_shop)
DTww_obs = HC_data[50][1] - HC_data[5][1]

if  DTww_exp - DTww_obs > 5.:
    ff = 'c.Air Cooler water temperature difference is high, possible AC fouling at water side'
    ff_all.append(ff)
#else:
#    print 'c.Air Cooler water temperature difference is OK'
    

### 3. Turbocharger
#print '3. Turbocharger'

print 'TC efficiencies:'
print 'Observed Compressor efficiency is: %.2f'%   (HC_data[83][1]*100)
print 'Expected Compressor efficiency is: %.2f'%   (HC_data[83][0]*100)

if diff[83]*100 < -5:
    ff = 'Compressor efficiency is reduced'
    ff_all.append(ff)
elif diff[83]*100 >5:
    ss = 'Check Pscav or TC speed measurement, compressor efficiency is high'
    k +=1; sensor_warning.append(ss)
print 'Observed Turbocharger efficiency is: %.2f'% (HC_data[85][1]*100)
print 'Observed Turbine efficiency is: %.2f'%      (HC_data[84][1]*100)
print 'Expected Turbine efficiency is: %.2f'%      (HC_data[84][0]*100)
print 'Expected Turbine efficiency (HC) is: %.2f'% (HC_data[44][0]*100)

# Compare Turbine Efficiency difference observed vs expected

# error_margin[84]
if diff[84]*100 > 3:
    ss = 'Turbine efficiency is increased - possible error in Texh or Pexh measurement'
    k +=1; sensor_warning.append(ss)
elif diff[84]*100 < -3:
    # 'Turbine efficiency is reduced'
        
    if fs[23] == 1:
        ff = 'a. Turbine efficiency is reduced. Increased Texh - \
        if no Turbine Issue is detected in the main algorithm, \
        which uses more data then the increase in temperature \
        and subsequent drop of T eff is not due to a Turbine fault'
        ff_all.append(ff)
    if fs[22] == 1:
        ff = 'b. Turbine efficiency is reduced. Increased Pexh - \
        if no Turbine Issue is detected in the main algorithm, \
        which uses more data then the increase in pressure and \
        subsequent drop of T eff is not due to a Turbine fault'
        ff_all.append(ff)
#else:
#    print 'Turbine is OK'
#    print
    
# Try to validate this with engine faults - verify the results of main diagnosis!


###############################################################################
#-------------------------MAIN BODY OF THE PROGRAM----------------------------#
###############################################################################

fs_rows = len(fault_symptom) # Number of faults in fault-symptom matrix
fs_cols = len((fault_symptom)[0])

# Create the array for comparison from the HC_data
measurement = fs_cols*[1] # Initialize a list of ones
#measurement[0]  = fs[23] # 01. Texh
#measurement[1]  = fs[19] # 02. Pscav
#measurement[2]  = fs[18] # 03. TC speed
#measurement[3]  = fs[80] # 04. Pcomp/Pscav
#measurement[4]  = fs[17] # 05. Pmax
#measurement[5]  = fs[16] # 06. Pcomp
#measurement[6]  = fs[14] # 07. Indicated Power
#measurement[7]  = fs[25] # 08. Pmax-Pcomp
#measurement[8]  = fs[22] # 09. Pexh
#measurement[9]  = fs[20] # 10. Tscav
#measurement[10] = fs[15] # 11. Shaft Power
#measurement[11] = fs[81] # 12. TC speed/ Pscav


# Different mapping for component analysis
#measurement[0]  = fs[16] # 01. Pcomp
#measurement[1]  = fs[17] # 02. Pmax
#measurement[2]  = fs[80] # 03. Pcomp/Pscav
#measurement[3]  = fs[25] # 04. Pmax-Pcomp
#measurement[4]  = fs[23] # 05. Texh
#measurement[5]  = fs[18] # 06. TC speed
#measurement[6]  = fs[81] # 07. TC speed/ Pscav
#measurement[7]  = fs[19] # 08. Pscav
#measurement[8]  = fs[22] # 09. Pexh
#measurement[9]  = fs[20] # 10. Tscav


# Construct the component table which will iterate over the fault-symtom matrix
# to find the faults for each component (cylinder, TC, etc.)
n_Cylinders = 6
n_TCs = 2
cylinders = n_Cylinders*[len(component_data)*[0.]]
TCs = n_TCs*[len(component_data)*[0.]]

for i in range(n_Cylinders):
    cyl = len(component_data)*[0]
    for k in [0,1,2,3]:
        cyl[k] = component_data[k][i]
    cyl[4] = fs[23]
    cyl[5] = fs[18]
    cyl[6] = fs[81]
    cyl[7] = fs[19]
    cyl[8] = fs[22]
    cyl[9] = fs[20]
    cylinders[i] = cyl     
    
for i in range(n_TCs):
    TC = len(components)*[0]
    TC[0] = fs[16]
    TC[1] = fs[17]
    TC[2] = fs[80]
    TC[3] = fs[25]
    TC[4] = fs[23]
    print TC
    for k in [5,6]:
        TC[k] = components[k][i]
    TC[7] = fs[19]
    TC[8] = fs[22]
    TC[9] = fs[20]
    TCs[i] = TC


# Check if the symptoms in measurement are above the limit for all
# the available faults in the fault-symptom matrix
#print 

#print 'SECTION 4 - Main Algorithm:'
# Separate the algorithm in 3 parts:
# A. Cylinder diagnosis
# B. Turbocharger diagnosis
# C. Overall diagnosis
all_faults = []
for cyl in cylinders:
    cylinder_faults = []
    for i in range(len(fault_symptom_cyl)):
        ratio = 0.
        c = 0
        n100 = fs_cols
        for j in range(fs_cols):
            if cyl[j] == fault_symptom_cyl[i][j]:
                c += 1 # if the symptom is detected the counter increases
            if fault_symptom_cyl[i][j] == 100:
                n100 -= 1 # if a symptom is not mapped then the denominator decreases
            if cyl[cr[i]] == fault_symptom_cyl[i][cr[i]]:
                crOK = dominant
            else:
                crOK = 0.
        print c, n100, crOK
        ratio = c/n100 *(100-dominant) + crOK
#        print c/n100*100, ratio
        if ratio >= limit:
            cylinder_faults.append([faults_cyl[i], ratio])
            print cylinder_faults
    all_faults.append(cylinder_faults)
#print
#obs_faults = []
#for i in range(fs_rows):
#    ratio = 0.
#    c = 0. # counter
#    n100 = fs_cols # initial number of columns
#    for j in range(fs_cols):
#        if measurement[j] == fault_symptom[i][j]:
#            c += 1 # if the symptom is detected the counter increases
#        if fault_symptom[i][j] == 100:
#            n100 -= 1 # if a symptom is not mapped then the denominator decreases
#        if measurement[cr[i]] == fault_symptom[i][cr[i]]:
#            crOK = dominant
#        else:
#            crOK = 0.
##    print c, n100, crOK
#    ratio = c/n100 *(100-dominant) + crOK
##    print c/n100*100, ratio
#    if ratio >= limit:
#        obs_faults.append([faults[i], ratio])
##        print faults[i]+ ' {:.2f}%'.format(ratio)
#        ff_all.append(faults[i])
#obs_faults.sort(reverse = True, key = lambda x: float(x[1]))

#for i in obs_faults: 
#    print i[0], '{:.2f}'.format(i[1])+'%'


#-----------------------------------------------------------------------------#
#-------------------------------- PRINTING -----------------------------------#
#-----------------------------------------------------------------------------#

# Observations
#print 'Obsrevations:' 
#for observation in observations:
#    print observation
#
## Sensor Warnings!
##print k
#print
#print 'Sensor Warnings:'
#if k == 0:
#    print 'NO SENSOR WARNINGS DETECTED'
#else:
#    for sw in sensor_warning:
#        print sw
#
#print
#print 'Possible Faults:'       
## Possible Faults
#if ff_all ==[]:
#    print 'No faults detected from main algorithm'
#else:
#    for ff in ff_all:
#        print ff 
        
        
