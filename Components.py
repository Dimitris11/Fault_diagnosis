# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 17:08:26 2015

@author: dimitris
"""
#map(f, sequence)
#is directly equivalent (*) to:
#[f(x) for x in sequence]
import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate

Load = np.array([25, 50, 75, 90, 100, 110], dtype ='float')/100.

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
#plt.plot(Load, AF_shop, x , y( x ), 'o')
    
### 2. Air Cooler

# Step 1 - Check Pressure Drop
if HC_data[21,4] ==  1:
    print 'The AC is fouled at the air side'
if HC_data[21,4] == -1:
    print 'The AC has very small pressure drop:'
    print 'a. Check pressure drop measurement'
    print 'b. If measurement is OK then there might be a significant reduction in the air flow'
# the last statement has to be checked
    
# Step 2 - Calculate and check effectiveness (high on low loads, lower on higher)
eff_AC = (HC_data[24]-HC_data[43])/(HC_data[24]-HC_data[5])




    


