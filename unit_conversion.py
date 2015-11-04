# -*- coding: utf-8 -*-
"""
Created on Wed Nov 04 15:17:53 2015

@author: dimitris
"""

def_unit = 'mbar' # unit to which we wish to convert

# Pressure unit dictionary (in database)
pr_conv = {}
pr_conv['mmW'] = 9.80665
pr_conv['mbar'] = 100.
pr_conv['bar'] = 10.**5

## Data read from excel file
# Raw data units dictionary 
raw_units = {}
raw_units['AF_dp'] = 'mmW'
raw_units['Engine Speed'] = 'rpm'

# Final data units dictionary
final_units = {}
final_units['AF_dp'] = 'mbar'
final_units['Engine Speed'] = 'rpm'

# Raw data values dictionary
raw_data = {}
raw_data['AF_dp'] = 25.0
raw_data['Engine Speed'] = 75.6

# Convert units and save to new dictionary named 'final_data'
final_data = {}

for parameter in raw_data:    
    unit1 = raw_units[parameter]
    print unit1
    unit2 = final_units[parameter]
    print unit2
    conversion_factor = pr_conv[unit1]/pr_conv[unit2]
    print conversion_factor
    final_data[parameter] = raw_data[parameter] *conversion_factor

    
print final_data


df1 = [1,1,1,2,2,2,2,4,4,5]
df2 = [5,2,4,3,1,5,4,1,2,2]

from collections import defaultdict
d = defaultdict(list)
for i, j in zip(df1,df2):
    d[i].append(j)