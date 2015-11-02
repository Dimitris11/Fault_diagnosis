# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 15:19:04 2015

@author: dimitris
"""

import numpy as np
from lourandos import *
import scipy.interpolate, scipy.optimize
from scipy import inf
import matplotlib.pyplot as plt

vessel_name = 'CAP PHILIPPE';
loading   = 1 # 1 if vessel is loaded, 0 if in ballast condition
limit     = 50. # Percentage ( % )
dominant  = 20. # Percentage ( % )
filename1 = 'Fault_Symptom_matrix.csv'
#filename2 = 'Philippe_01_2007.csv'
filename2 = 'CAP_THEODORA_06-2014.csv'

###############################################################################
#----------------------DATA FROM SHOP/SEA FOR CORRELATIONS--------------------#
###############################################################################

### Constants = [μ, Dc, γAir, γG, Pmcr, Nmcr]
const = np.array([0.72, 0.73, 1.4, 1.36, 18660, 91], dtype = 'float')

rpm_min = 50.0; rpm_MCR = 91.0; rpm_max = 93.9
power_min =  2500.; power_max = 20000.

### Data from SHOP TEST
Load = np.array([25, 50, 75, 90, 100, 110], dtype ='float') /100.
rpm_shop = np.array([ 57.4, 72.3, 82.6, 87.9, 91,	93.9 ], dtype ='float')
power_shop = np.array([ 4313,	 8475, 12761, 15376, 17121, 18732 ], dtype ='float')
eff_mech_shop = np.array([0.871346791, 0.913658654, 0.933402422, \
0.940307356, 0.944465013, 0.944609484], dtype = 'float')
Pscav_shop = np.array([1.38058, 2.13032, 2.93965, 3.43898, 3.80898, 4.06898], dtype ='float')
pscav_pexh_shop = [0.07, 0.15, 0.20, 0.29, 0.28, 0.24]
backpressure_shop = np.array([0, 3.92266, 7.84532, 14.709975, 15.69064, 22.555295], dtype = 'float') # mbar

### Data from SEA TRIALS
# Corrected FPI for Sea Trials simulation with ThermoS
FPI_sea = np.array([72.33, 75.33, 80, 84.17, 85.33, 88.17], dtype ='float')
# Indicated Power from sea trials simulation with ThermoS
power_ind_sea_sim = np.array([13425.5, 14014, 15870, 16695, 17517.4, 18042], dtype ='float')
egb_drop = 5 # mbar

### Data from both SHOP/SEA
rpm_trials = np.array([57.4, 72.3, 82.6, 87.9	, 91, 93.9, 85.9,	85.9, 90.9,\
90.69, 94.09], dtype = 'float')
DTww_trials = np.array([1.5, 5.5, 13, 16.5, 21.5, 25.5, 17, 14.5, 21.5, \
20, 26.5], dtype = 'float')

###############################################################################
#-----------------------GETTING INITIAL DATA FROM FILES-----------------------#
###############################################################################
print
############ Import data from files and store to arrays/list ##################

#read and store the FAULTS csv as numpy array
row_count, fulltable = create_table(filename1)
#fault_symptom = fulltable[1:row_count]
fault_symptom = [x[2:len(x)] for x in fulltable[1:row_count]]
fault_symptom = np.array([ map(float,x) for x in fault_symptom ])
# Critical parameter Indices
cr = np.array( [ x[1] for x in fulltable[1:row_count] ], dtype = 'int' )
# Store the engine's parameters(symptoms) in a list
parameters = fulltable[1:]
# Store the engine's possible faults in a list
faults = [fulltable[i][0] for i in range(1, row_count)]

#read and store the MEASUREM csv as numpy array
row_count2, fulltable2 = create_table(filename2)
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
if HC_data[48,1] == 0: # Backpressure is not recorded
    a = np.polyfit(rpm_shop, backpressure_shop, 3)  
    backpressure = a[0]*HC_data[1,1]**3 + a[1]*HC_data[1,1]**2 + a[2]*HC_data[1,1] + a[3] 
    HC_data[48,0] = HC_data[48,1] = backpressure
if HC_data[49,1] == 0:
    HC_data[49,1] = HC_data[49,0] = egb_drop

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
error_margin = np.zeros(len(HC_data)) # Initialize deviation for each parameter
fs = np.zeros(len(HC_data)) # Initialize an array of zeros to store the -1, 0, 1 

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

#f = scipy.interpolate.interp1d( rpm_shop, power_shop, kind='cubic' )

# Define the power function of the fitting curve 
def power_func (x, a, b):
    return a*x**b

factors, b = scipy.optimize.curve_fit(power_func, rpm_shop, power_shop, p0 = (0.02, 3.))
a = factors[0]; b = factors[1]

if HC_data[1,1]*1.2 < rpm_max:
    rpm_max = HC_data[1,1]*1.2
if HC_data[1,1]*0.8 > rpm_min:
    rpm_min = HC_data[1,1]*0.8
    
rpm = np.linspace(rpm_min, rpm_max, 200)
power1 = a*rpm**b       # Shop Test Curve
power2 = 0.90*a*rpm**b  # Sea Trials Curve
power3 = 0.75*a*rpm**b  # Light Running Curve
power = a*HC_data[1,0]**b # expected shop curve power for the specific speed
torque_index = HC_data[15,1]/power  # for FPI calculation
torque_index2 = HC_data[54,1]/power # from Torsion meter

# PLOTTING of Load Diagram 
plt.figure(1)
plt.plot(rpm, power1, color = 'b', label = 'Shop Test')
plt.plot(rpm, power2, color = 'orange', label = 'Sea Trials')
plt.plot(rpm, power3, color = 'g', label = 'Light Curve -75%')
plt.plot([rpm_MCR, rpm_MCR], [0.65*a*rpm_MCR**b, 1.1*a*rpm_MCR**b], 'k--')
plt.plot(HC_data[1,1], HC_data[15,0], 'cx', label = 'Expected', markersize =6, mew = 3)
plt.plot(HC_data[1,1], HC_data[15,1], 'ro', label = 'Observed - Indicator')
if HC_data[54, 1] != 0:
    plt.plot(HC_data[1,1], HC_data[54,1], 'm+', label = 'Observed - Torsion meter', markersize =6, mew = 3)
plt.title('Load Diagram', fontsize = 17)
plt.xlabel('Engine Speed (rpm)')
plt.ylabel('Shaft Power (kW)')
plt.grid(True)
plt.legend(loc = 2)
plt.show()

print
print 'Observed - Indicator diagram:' 
if torque_index > 1.0:
    if loading == 0:
        print 'Power is too high possible error in measurement'
    else:
        print 'The engine operates in the torque rich region (overloaded)'
elif torque_index <=1.0 and torque_index >0.9:
    if loading == 1:
        print 'The engine operates in normal load'
    else:
        print 'The engine load is high - if hull and weather conditions are OK, check measurement'
elif torque_index <0.9 and torque_index >0.8:
    if loading == 1:
        print 'The engine load is low - check measurement'
    else:
        print 'The engine operates in normal load'
else:
    if loading == 1:
        print 'The engine load is very low - check measurement' 
    else:
        print 'The engine load is low - check measurement'
print
if HC_data[54,1] != 0: 
    print 'Observed - Torsion meter:'
    if torque_index2 > 1.0:
        if loading == 0:
            print 'Power is too high possible error in measurement'
        else:
            print 'The engine operates in the torque rich region (overloaded)'
    elif torque_index2 <=1.0 and torque_index2 >0.9:
        if loading == 1:
            print 'The engine operates in normal load'
        else:
            print 'The engine load is high - if hull and weather conditions are OK, check measurement'
    elif torque_index2 <0.9 and torque_index2 >0.8:
        if loading == 1:
            print 'The engine load is low - check measurement'
        else:
            print 'The engine operates in normal load'
    else:
        if loading == 1:
            print 'The engine load is very low - check measurement' 
        else:
            print 'The engine load is low - check measurement'
        
        
# 2nd - FPI vs Pi (or Indicated Power)

a = np.polyfit(power_ind_sea_sim, FPI_sea, 1)
b = np.polyfit(FPI_sea, power_ind_sea_sim, 1)

if HC_data[14,1]*1.2 < power_max:
    power_max = HC_data[14,1]*1.2
if HC_data[14,1]*0.75 > power_min:
    power_min = HC_data[14,1]*0.75

power_sea = np.linspace(power_min, power_max, 3)
fpi = a[0]*power_sea + a[1]
fpi_exp = a[0]*HC_data[14,1] + a[1]
power_exp = b[0]*HC_data[7,1] + b[1]

fpi_diff = (HC_data[7,1] - fpi_exp)/ HC_data[7,1] *100 # ( % )
power_diff = (HC_data[14,1] -power_exp)/ HC_data[14,1] *100 # ( % )

# PLOTTING of FPI vs Indicated Power 
plt.figure(2)
#plt.plot(power_ind_sea_sim, FPI_sea, 'g+', label = 'Sea Trial data')
plt.plot(power_sea, fpi, 'b--', linewidth = 2, label = 'Sea Trials')
plt.plot(HC_data[14,1], HC_data[7,1], 'ro', label = 'Operating point')
plt.title('FPI vs Indicated Power', fontsize = 17)
plt.xlabel('Indicated Power (kW)')
plt.ylabel('Fuel Pump Index (-)')
plt.grid(True)
plt.legend(loc = 2)
plt.show()

if power_diff < 1 and power_diff > -1:
    print 'There is good correlation between FPI and indicated power'
else:
    print 'FPI is not well correlated with indicated power - possible FPI offset or error in measurements'

print
# 3rd - Mechanical Efficiency (no good correlation with speed)


##def log_func(x, a):
##    return a*np.log(x)
##def sqrt_func(x, a):
##    return a*np.sqrt(x)
##A, cc = scipy.optimize.curve_fit(sqrt_func, rpm_shop, eff_mech_shop)
#co = np.polyfit(rpm_shop, eff_mech_shop, 2)
#a= co[0]; b = co[1]; c = co[2]
#eff_m_fit = a*rpm**2 + b*rpm + c
#
#figure(3)
#plt.plot(rpm, eff_m_fit, 'b-')
#plt.plot(HC_data[1,1], HC_data[87,0], 'ro')


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

f = scipy.interpolate.interp1d( rpm_shop, pscav_pexh_shop )
pscav_pexh = f(HC_data[1,1])
     
if HC_data[82,1] < 0.1 or HC_data[82,1] > 0.3:
    print "Check scavenge pressure or exhaust gas pressure because of #9a"
    k +=1
elif HC_data[82,1] > pscav_pexh +0.1:
    print "Check scavenge pressure or exhaust gas pressure because of #9b"
    k +=1
elif HC_data[82,1] < pscav_pexh -0.1:
    print "Check scavenge pressure or exhaust gas pressure because of #9b"
    k +=1
    
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

#11. Shaft (FPI) vs Shaft from Torsion meter
if abs((HC_data[54,1] - HC_data[15,0])/HC_data[54,1] *100) < 2:
    HC_data[54,4] = 0 # Shaft power is OK
else:
    print 'Check Torsion meter or FPI measurement'
  

#12. Mechanical Efficiency
    
eff_m = HC_data[54,1]/HC_data[14,1]
if eff_m > 0.98:
    k +=1
    if HC_data[54,4] == 0:
        print 'Check Indicated Power measurement (low), very high mechanical efficiency'
    else: 
        print 'Check both Torsion meter and Indicated Power measurement, efficiency > 1'
elif eff_m < 0.85:
    k +=1
    if HC_data[54,4] == 0:
        print 'Check Indicated Power measurement (high), very low mechanical efficiency'
    else:
        print 'Check both Torsion meter and Indicated Power measurement, efficiency < 0.85'

    
#12. Turbocharger Efficiency

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
    ratio = 0.
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

### 1. AIR FILTER
print '1. Air Filter'
# Step 1 - Build the Correlation from Shop Test
AF_shop = np.array([0.000490333,	0.001372931, 0.002745862,	0.003285228, 0.00392266, 0.004511059])
# Step 2 - Interpolate Shop Test data and find the expected pressure drop
f = scipy.interpolate.interp1d( Pscav_shop, AF_shop )
AF_exp = f(HC_data[19,1])
AF_obs = HC_data[0,1]
# Step 3 - Compare observed and expected value and display message
AF_diff = (AF_obs - AF_exp)/AF_obs 
if AF_diff >= 0.4:
    print 'Air Filter is fouled and needs to be cleaned'
elif AF_diff < 0.:
    print 'AIr Filter pressure drop is less than normal - check measurement'
print  

plt.figure(3)
plt.plot(Pscav_shop, AF_shop, 'b-', label = 'Expected AF pr.drop')
plt.plot(HC_data[19,1], AF_obs, 'ro', label = 'Observed AF pr. drop')
plt.title('Air Filter', fontsize = 17)
plt.ylim([0., AF_obs*1.3])
plt.xlabel('Scavenge Pressure (bar)')
plt.ylabel('Air Filter Pressure drop (mbar)')
plt.grid(True)
plt.legend(loc = 2)
plt.show()

### 2. Air Cooler
print '2. Air Cooler'
# Step 1 - Check Pressure Drop
if HC_data[21,4] ==  1:
    print 'a.The Air Cooler is fouled at the air side'
if HC_data[21,4] == -1:
    if HC_data[18,4] == -1.0:
        print 'a.Possible reduction of air flow rate through Air Cooler'
    else:
        print 'a.Check Air Cooler pressure drop measurement'

# Step 2 - Calculate and check effectiveness (high on low loads, lower on higher)
eff_AC = (HC_data[24,1]-HC_data[43,1])/(HC_data[24,1]-HC_data[5,1])
# limit, should be < 0.85
if eff_AC < 0.88:
    print ''
elif eff_AC >= 0.98:
    print 'b.Air Cooler Effectiveness is high, check Air Cooler Delivery Temperature'
else:
    print 'b.Air Cooler Effectiveness is OK'

# Step 3 - Calculate DTww and correlate with data from shop/sea trials
a = np.polyfit(rpm_trials, DTww_trials, 2)
DTww_exp = a[0]*HC_data[1,1]**2 + a[1]*HC_data[1,1] + a[2]
DTww_obs = HC_data[50,1] - HC_data[5,1]


if DTww_obs - DTww_exp > 3.:
    print 'c.Air Cooler water temperature difference is high, possible AC fouling at water side'
else:
    print 'c.Air Cooler water temperature difference is OK'
    
plt.figure(4)
plt.plot(rpm,(a[0]*rpm**2 + a[1]*rpm + a[2]), 'b-', label = 'Water Temp. difference at AC from Shop-Sea')
plt.plot(HC_data[1,1], DTww_obs, 'ro', label = 'Observed Water Temp. difference at AC')
plt.title('Air Cooler Water Temperature Difference', fontsize = 17)
#plt.ylim([0., AF_obs*1.3])
plt.xlabel('Engine speed (rpm)')
plt.ylabel('Temperature difference (°C)')
plt.grid(True)
plt.legend(loc = 3)
plt.show()
print 

### 3. Turbocharger
print '3. Turbocharger'

print 'Observed Compressor efficiency is: %.2f'%   (HC_data[83,1]*100)
print 'Expected Compressor efficiency is: %.2f'%   (HC_data[83,0]*100)
if HC_data[83,2] < 3.:
    print 'Compressor is OK'
    
print 'Observed Turbocharger efficiency is: %.2f'% (HC_data[85,1]*100)
print 'Observed Turbine efficiency is: %.2f'%      (HC_data[84,1]*100)
print 'Expected Turbine efficiency is: %.2f'%      (HC_data[84,0]*100)
print 'Expected Turbine efficiency (HC) is: %.2f'% (HC_data[44,0]*100)

# Compare Turbine Efficiency difference observed vs expected
turb_diff = (HC_data[84,1] - HC_data[84,0])*100
# error_margin[84]
if HC_data[84,2]*100 > 3:
    print 'Turbine efficiency is increased - possible error in Texh or Pexh measurement'
    print
elif HC_data[84,2]*100 < -3:
    print 'Turbine efficiency is reduced'
    print    
    if HC_data[23, 4] == 1:
        print 'a. Increased Texh - if no Turbine Issue is detected in the main algorithm, \
        which uses more data then the increase in temperature and subsequent drop of T eff \
        is not due to a Turbine fault'
        print
    if HC_data[22, 4] == 1:
        print 'b. Increased Pexh - if no Turbine Issue is detected in the main algorithm, \
        which uses more data then the increase in pressure and subsequent drop of T eff \
        is not due to a Turbine fault'
        print
else:
    print 'Turbine is OK'
    print
    
# Try to validate this with engine faults - verify the results of main diagnosis!


print 'APPENDIX'
print
j=4
for i in [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 80, 81, 83, 84, 85]:
    check_meas_OK( parameters_all[i],HC_data[i,j-2], HC_data[i,j], units[i] )

#plt.close('all')




