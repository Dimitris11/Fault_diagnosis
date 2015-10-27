# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 11:45:34 2015

@author: dimitris
"""

import matplotlib.pyplot as plt
import scipy.interpolate
import scipy.optimize

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
plt.plot(HC_data[1,1], HC_data[15,0], 'cx', label = 'Expected', markersize =6, mew = 3)
plt.plot(HC_data[1,1], HC_data[15,1], 'ro', label = 'Pressure Trace')
plt.plot(HC_data[1,1], HC_data[54,1], 'm+', label = 'Torsion meter', markersize =6, mew = 3)
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

# 3rd - Mechanical Efficiency (no good correlation with speed)

#eff_mech_shop = np.array([0.871346791, 0.913658654, 0.933402422, \
#0.940307356, 0.944465013, 0.944609484], dtype = 'float')
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

# 4th - Pscav - Pexh









