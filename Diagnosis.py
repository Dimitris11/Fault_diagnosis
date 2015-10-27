# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 14:29:20 2015
Fault Diagnosis 
@author: Dimitris Lourandos
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate, scipy.optimize
from lourandos import check_meas2, create_table
from scipy import inf

#cases = range(240,245) # exclude zeros
limit     = 40. # Percentage ( % )
dominant  = 20. # Percentage ( % )
filename1 = 'Fault_Symptom_matrix.csv'
filename2 = 'Philippe_01_2007.csv'
#filename2 = 'CAP_THEODORA_06-2014.csv'

###############################################################################
#-----------------------GETTING INITIAL DATA FROM FILES-----------------------#
###############################################################################
print
# Constants = [μ, Dc, γAir, γG, Pmcr, Nmcr]
const = np.array([0.72, 0.73, 1.4, 1.36, 18660, 91], dtype = 'float')


#read and store the FAULTS csv as numpy array
row_count, fulltable = create_table(filename1)
#fault_symptom = fulltable[1:row_count]
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
# Calculate Mechanical Efficiency
eff_m = HC_data[15]/HC_data[14]
HC_data = np.row_stack(( HC_data,Pcomp_Pscav, Tc_Pscav, Pscav_Pexh, eff_C,\
eff_T, eff_TC, load_i, eff_m ))
parameters_all.extend(['Pcomp_Pscav', 'Tc_Pscav', 'Pscav_Pexh', 'eff_C',\
'eff_T', 'eff_TC', 'Load', 'Mechanical efficiency'])

# Calculate differences and append to HC_data
ex = HC_data[:,0] 
obs = HC_data[:,1]
diff = obs-ex
diff_percent = diff/obs*100
error_margin = np.zeros(len(HC_data))
fs = np.zeros(len(HC_data))

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
error_margin[87]= 3  # Error margin for engine mechanical efficiency


units = []
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
    s = parameters_all[i]
    if '[' in s: units.append(s[s.find("[")+1:s.find("]")])
    else: units.append(' ')   
            
# Create the final numpy array (matrix), 52 rows (parameters) x 5 cols 
HC_data = np.column_stack(( HC_data, diff, diff_percent, fs ))

HC_rows = int(np.shape(HC_data)[0])
HC_cols = int(np.shape(HC_data)[1])

###############################################################################
#---------------------------PLOTTING OF BASIC DATA----------------------------#
###############################################################################

print 'SECTION 1 - Diagrams'
print
# 1st - Load Diagram

rpm_shop = np.array([ 57.4, 72.3, 82.6, 87.9, 91,	93.9 ], dtype ='float')
power_shop = np.array([ 4313,	 8475, 12761, 15376, 17121, 18732 ], dtype ='float')

#f = scipy.interpolate.interp1d( rpm_shop, power_shop, kind='cubic' )
# Define the power function of the fitting curve 
def power_func (x, a, b):
    return a*x**b
    

factors, b = scipy.optimize.curve_fit(power_func, rpm_shop, power_shop, p0 = (0.02, 3.))
a = factors[0]
b = factors[1]

rpm_min = 50.0
rpm_MCR = 91.0
rpm_max = 93.9
if HC_data[1,1]*1.2 < rpm_max:
    rpm_max = HC_data[1,1]*1.2
if HC_data[1,1]*0.8 > rpm_min:
    rpm_min = HC_data[1,1]*0.8
    
rpm = np.linspace(rpm_min, rpm_max, 200)
power1 = a*rpm**b
power2 = 0.90*a*rpm**b
power3 = 0.75*a*rpm**b
power = a*HC_data[1,0]**b
torque_index = HC_data[15,1]/power


plt.figure(1)
plt.plot(rpm, power1, color = 'b', label = 'Shop Test')
plt.plot(rpm, power2, color = 'orange', label = 'Sea Trials')
plt.plot(rpm, power3, color = 'g', label = 'Light Curve -75%')
plt.plot([rpm_MCR, rpm_MCR], [0.65*a*rpm_MCR**b, 1.1*a*rpm_MCR**b], 'k--')
plt.plot(HC_data[1,1], HC_data[15,0], 'rx', label = 'Expected', markersize =6, mew = 3)
plt.plot(HC_data[1,1], HC_data[15,1], 'ro', label = 'Operating Point')
plt.title('Load Diagram', fontsize = 17)
plt.xlabel('Engine Speed (rpm)')
plt.ylabel('Shaft Power (kW)')
plt.grid(True)
plt.legend(loc = 2)
plt.show()

# 2nd - FPI vs Pi (or Indicated Power)

FPI_sea = np.array([72.33, 75.33, 80, 84.17, 85.33, 88.17], dtype ='float')
power_ind_sea_sim = np.array([13425.5, 14014, 15870, 16695, 17517.4, 18042], dtype ='float')
coeffs = np.polyfit(power_ind_sea_sim, FPI_sea, 1)
a = coeffs[0]; b = coeffs[1]

power_min =  2500.
power_max = 20000.
if HC_data[14,1]*1.2 < power_max:
    power_max = HC_data[14,1]*1.2
if HC_data[14,1]*0.8 > power_min:
    power_min = HC_data[14,1]*0.8

power_sea = np.linspace(power_min, power_max, 3)
fpi = a*power_sea + b

plt.figure(2)
#plt.plot(power_ind_sea_sim, FPI_sea)
plt.plot(power_sea, fpi, 'b--', linewidth = 2, label = 'Sea Trials')
plt.plot(HC_data[14,1], HC_data[8,1], 'ro', label = 'Operating point')
plt.title('FPI vs Indicated Power', fontsize = 17)
plt.xlabel('Indicated Power (kW)')
plt.ylabel('Fuel Pump Index (-)')
plt.grid(True)
plt.legend(loc = 2)
plt.show()

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
print
print 'Now the sensor check starts:' 
# 1. Pscav 
if HC_data[19,j] !=0 and HC_data[16,j] ==0:
    print 'a. Check Scavenge Pressure measurement\
    b. Check Exhaust valve timing because of #1'
    k +=1
# 2. BSFC
if HC_data[12,j] !=0 and HC_data[17,j] ==0 and HC_data[23,j] ==0 and \
HC_data[18,j] ==0 and HC_data[14,j] ==0:
    print 'Check Fuel Consumption or Power measurement because of #2'
    k +=1
# 3. TDC Correction
if HC_data[17,j] ==0 and HC_data[16,j] ==0 and HC_data[14,j] !=0:
    print 'a.Check pressure diagram measurement\
    b. TDC correction procedure because of #3'
    k +=1
# 4. TC speed
if HC_data[18,j] !=0 and HC_data[23,j] ==0 and HC_data[19,j] ==0 and \
HC_data[17,j] ==0 and HC_data[14,j] ==0:
    print "Check Turbocharger Speed measurement because of #4"
    k +=1
# 5. Torsion Meter
if HC_data[15,j] !=0 and HC_data[23,j] ==0 and HC_data[19,j] ==0 and \
HC_data[17,j] ==0 and HC_data[16,j] ==0 and HC_data[14,j] ==0:
    print 'Please check Torsion Meter reading because of #5'
    k +=1
# 6. Exhaust Gas Temperature     
if HC_data[23,j] !=0 and HC_data[17,j] ==0 and HC_data[18,j] ==0 and \
HC_data[14,j] ==0:
    print 'Check for faulty exhaust receiver temperature\
    sensor because of #6'
    k +=1
#7. Texhaust & TC speed
if HC_data[23,j] ==1 and HC_data[18,j] ==-1:
    print 'Check for faulty exhaust receiver temperature sensor\
    and turbocharger speed measurement because if #7'
if HC_data[23,j] ==-1 and HC_data[18,j] ==1:
    print 'Check for faulty exhaust receiver temperature sensor\
    and turbocharger speed measurement because if #7'
    k +=1
#8. Scavenge pressure and TC speed
if HC_data[19,j] ==-1 and HC_data[18,j] == 1:
    print 'Check scavenge pressure because of #8'
if HC_data[19,j] == 1 and HC_data[18,j] ==-1:
    print 'Check scavenge pressure because of #8'
    k +=1   
#9. Pscav - Pexh  
pscav_pexh_shop = [0.07, 0.15, 0.20, 0.29, 0.28, 0.24]
f = scipy.interpolate.interp1d( rpm_shop, pscav_pexh_shop )
pscav_pexh = f(HC_data[1,1])      
if HC_data[82,1] < 0.1 or HC_data[82,1] > 0.3:
    print "Check scavenge pressure or exhaust gas pressure because of #9a"
    k +=1
elif HC_data[82,1] > pscav_pexh +0.1:
    print "Check scavenge pressure or exhaust gas pressure because of #9b"
elif HC_data[82,1] < pscav_pexh -0.1:
    print "Check scavenge pressure or exhaust gas pressure because of #9b"
#10. Compressor Efficiency
if HC_data[83,1] > 0.9:
    print "Check for high Pscav or low TC speed measurements because\
    compressor isentropic efficiency is {:.2f} when it\
    should be < 0.90".format(HC_data[83,1])
if HC_data[83,1] < 0.75:
    print "Check for low Pscav or high TC speed measurements because\
    compressor isentropic efficiency is {:.2f} when it\
    should be > 0.75".format(HC_data[83,1])
    k +=1
#12. Mechanical Efficiency
eff_diff = HC_data[87,2]*100; shaft_diff = HC_data[15,4]
if abs(eff_diff) <= 2:
#    pr = 'Mechanical efficiency is OK'
    p =  0;
elif eff_diff < 5. and eff_diff > 2.:
    pr = 'Mechanical efficiency is HIGH'
    p =  1; k+=1
elif eff_diff > -5. and eff_diff < -2.:
    pr = 'Mechanical efficiency is LOW'
    p = -1; k+=1
elif eff_diff < -5.:
    pr = 'Mechanical efficiency is VERY LOW'
    p = -2; k+=1
elif eff_diff > 5.:
    pr = 'Mechanical efficiency is VERY HIGH'
    p =  2; k+=1
else:
    pr = 'Something went wrong with mechanical efficiency'

try: print pr
except NameError: print 

if p == 0:
    if shaft_diff ==  0:
        pr2 =  'Indicated and Shaft is OK'
    if shaft_diff == -1:
        pr2 =  'Indicated and Shaft is Low - check both measurements, possible fault'
        k+=1
    if shaft_diff ==  1:
        pr2 =  'Indicated and Shaft are high - possible hull fouling'
        k+=1
elif p == 1:
    if shaft_diff ==  0:
        pr2 =  'Indicated Power is low - Check Measurement'
    if shaft_diff ==  1:
        pr2 =  'Indicated Power is OK, check Torsion Meter'    
elif p == -1:
    if shaft_diff == 1:
        pr2 =  'Indicated is OK and Shaft is Low - check Torsion Meter'
    if shaft_diff == 0:
        pr2 =  'Indicated is high and Shaft is OK - check Indicated'
elif p == 2:
    if shaft_diff ==  1:
        pr2 =  'Indicated is low and Shaft Power is high - check both'  
elif p == -2:
    if shaft_diff ==  1:
        pr2 =  'Indicated is high and Shaft Power is low - check both'
        
try: print pr2+' because of #11'
except NameError: print "No Fault"
    
#12. Turbocharger Efficiency
    
#    if meas[1] - meas_suppl[i][1] < 0.1 or meas[1] - meas_suppl[i][1] > 0.3:
#        print 'Problem in Scavenge or Exhaust pressure measurement'
#    elif meas[1] - meas_suppl[i][1] < 0.1:
#        print 'Small Pscav - Pexh difference - Pls check both measurements' 
#    elif meas[1] - meas_suppl[i][1] > 0.4:
#        print 'Very large Pscav - Pexh difference - Pls check both measurements'         
#    print
    
#print k
if k == 0:
    print 'NO SENSOR FAULTS DETECTED'    
    
    
    
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

print
print 'SECTION 5 - Components:'
print


Load = np.array([25, 50, 75, 90, 100, 110], dtype ='float') /100.
### 1. AIR FILTER

# Step 1 - Build the Correlation from Shop Test
AF_shop = np.array([0.000490333,	0.001372931, 0.002745862,	0.003285228, 0.00392266, 0.004511059])
# Step 2 - Interpolate Shop Test data and find the expected pressure drop
f = scipy.interpolate.interp1d( rpm_shop, AF_shop )
AF_exp = f(HC_data[1,1])
AF_obs = HC_data[0,1]
# Step 3 - Compare observed and expected value and display message
AF_diff = (AF_obs - AF_exp)/AF_obs 
if AF_diff >= 0.4:
    print 'Air Filter is fouled and needs to be cleaned'
    print
elif AF_diff < 0.:
    print 'AIr Filter pressure drop is less than normal - check measurement'
    print  
plt.plot(rpm_shop, AF_shop, 'b-', label = 'Expected AF pr.drop')
plt.plot(HC_data[1,1], AF_obs, 'ro', label = 'Observed AF pr. drop')
plt.title('Air Filter', fontsize = 17)
plt.xlabel('Engine Speed (rpm)')
plt.ylabel('Air Filter Pressure drop (mbar)')
plt.grid(True)
plt.legend(loc = 2)
plt.show()
### 2. Air Cooler

# Step 1 - Check Pressure Drop
if HC_data[21,4] ==  1:
    print 'The Air Cooler is fouled at the air side'
if HC_data[21,4] == -1:
    print 'The Air Cooler has pressure drop less than normal:'
    print 'a. Check pressure drop measurement'
    print 'b. If measurement is OK then there might be a significant reduction in the air flow'
    print
# the last statement has to be checked
    
# Step 2 - Calculate and check effectiveness (high on low loads, lower on higher)
#eff_AC = (HC_data[24]-HC_data[43])/(HC_data[24]-HC_data[5])
## limit, should be < 0.8
#if eff_AC >= 0.98:
#    print 'Scavenge temperature measurement is low, maybe reduced flow rate'
#if eff_AC <= 0.85:
#    print 'something'
#
#



### 3. Turbocharger

print 'Observed Compressor efficiency is: %.2f'%   (HC_data[83,1]*100)
print 'Observed Turbine efficiency is: %.2f'%      (HC_data[84,1]*100)
#print 'Expected Turbine efficiency is: ',      HC_data[84,0]
#print 'Expected Turbine efficiency (HC) is: ', HC_data[44,0]

# Compare Turbine Efficiency calculated with the one from HC
turb_diff = (HC_data[84,1] - HC_data[84,0])*100
if HC_data[84,2]*100 > error_margin[84]:
    print 'Turbine efficiency is increased - possible error in Texh or Pexh measurement'
    print
elif HC_data[84,2]*100 < -error_margin[84]:
    print 'Turbine efficiency is reduced'
    print    
    if HC_data[23, 4] == 1:
        print 'a. Increased Texh - if no Turbine Issue is detected in the main algorithm, \
        which uses more data then the increase in temperature and subsequent drop of T eff \
        is not due to a Turbine fault'
        print
    if HC_data[22, 4] == 1:
        print 'b. Increased Pexh'
        print
else:
    print 'Turbine is OK'
    print
    
