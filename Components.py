# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 17:08:26 2015

@author: dimitris
"""
#map(f, sequence)
#is directly equivalent (*) to:
#[f(x) for x in sequence]
import numpy as np
import scipy.interpolate

Load = np.array([25, 50, 75, 90, 100, 110], dtype ='float') /100.
### 1. AIR FILTER

# Step 1 - Build the Correlation from Shop Test
AF_shop = np.array([0.000490333,	0.001372931, 0.002745862,	0.003285228, 0.00392266, 0.004511059])
# Step 2 - Interpolate Shop Test data and find the expected pressure drop
f = scipy.interpolate.interp1d( Load, AF_shop )
AF_exp = f(load_i[0])
AF_obs = HC_data[0,1]
# Step 3 - Compare observed and expected value and display message
AF_diff = (AF_obs - AF_exp)/AF_obs 
if AF_diff >= 0.5:
    print 'Air Filter is fouled and needs to be cleaned'
    print
elif AF_diff < 0.:
    print 'AIr Filter pressure drop is less than normal - check measurement'
    print  
#plt.plot(Load, AF_shop, x , y( x ), 'o')
    
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
    
# Try to validate this with engine faults - verify the results of main diagnosis!
    
    
    
