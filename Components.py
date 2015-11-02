# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 17:08:26 2015

@author: dimitris
"""

import numpy as np
import scipy.interpolate

Load = np.array([25, 50, 75, 90, 100, 110], dtype ='float') /100.
Pscav_shop = np.array([1.38058, 2.13032, 2.93965, 3.43898, 3.80898, 4.06898], dtype ='float')
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
    print
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

# the last statement has to be checked

# Step 2 - Calculate and check effectiveness (high on low loads, lower on higher)
eff_AC = (HC_data[24,1]-HC_data[43,1])/(HC_data[24,1]-HC_data[5,1])
# limit, should be < 0.85
if eff_AC < 0.88:
    print ''
elif eff_AC >= 0.98:
    print 'b.Air Cooler Effectiveness is high, check Air Cooler Delivery Temperature'
else:
    print 'b.Air Cooler Effectiveness is OK'

# Step 3 - Calculate DTww and correlate with data from shop-sea
rpm_trials = np.array([57.4, 72.3, 82.6, 87.9	, 91, 93.9, 85.9,	85.9, 90.9,\
90.69, 94.09], dtype = 'float')
DTww_trials = np.array([1.5, 5.5, 13, 16.5, 21.5, 25.5, 17, 14.5, 21.5, \
20, 26.5], dtype = 'float')
coeffs2 = np.polyfit(rpm_trials, DTww_trials, 2)
a = coeffs2[0]; b = coeffs2[1]; c = coeffs2[2]
DTww_exp = a*HC_data[1,1]**2 + b*HC_data[1,1] + c
DTww_obs = HC_data[50,1] - HC_data[5,1]


if DTww_obs - DTww_exp > 3.:
    print 'c.Air Cooler water temperature difference is high, possible AC fouling at water side'
else:
    print 'c.Air Cooler water temperature difference is OK'
#Air Cooler fouled at water side
plt.figure(4)
plt.plot(rpm,(a*rpm**2 + b*rpm + c), 'b-', label = 'Water Temp. difference at AC from Shop-Sea')
plt.plot(HC_data[1,1], DTww_obs, 'ro', label = 'Observed Water Temp. difference at AC')
plt.title('Air Cooler Water Temperature Difference', fontsize = 17)
#plt.ylim([0., AF_obs*1.3])
plt.xlabel('Engine speed (rpm)')
plt.ylabel('Temperature (°C)')
plt.grid(True)
plt.legend(loc = 2)
plt.show()
print 

### 3. Turbocharger
print '3. Turbocharger'


print 'Observed Compressor efficiency is: %.2f'%   (HC_data[83,1]*100)
if HC_data[83,2] < 3.:
    print 'Compressor is OK'
print
print 'Observed Turbine efficiency is: %.2f'%      (HC_data[84,1]*100)
#print 'Expected Turbine efficiency is: ',      HC_data[84,0]
#print 'Expected Turbine efficiency (HC) is: ', HC_data[44,0]

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
    
    
    
