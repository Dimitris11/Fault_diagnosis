# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 10:03:02 2015

@author: dimitris
"""

def linear_interpolation(x, x_list, y_list):
    """ 
    Takes as arguments the x coordinate at which we eant to interoplate
    and two lists x,y that define the points of the function
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
        return 'x parameter is out of range'
        
                
y = linear_interpolation(57.3, rpm_shop, power_shop)
print y               