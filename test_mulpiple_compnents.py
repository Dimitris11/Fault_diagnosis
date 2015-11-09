# -*- coding: utf-8 -*-
"""
Created on Mon Nov 09 16:58:28 2015

@author: dimitris
"""

l1 = range(10)
l2 = range(100,110)
l3 = range(9,109,10)
#print l1+l2

ll = [l1,l2,l3]


print 'l1 = ', l1
print 'l2 = ', l2
print 'l3 = ', l3

ii =[0,1]
cyl = [[10*[0]] for x in xrange(6)]
for i in ii:
    
    for k in range(4):
        cyl[i][k] = ll[i+1][k]
        cyl[i][4:10] = ll[0][4:10]
    
print 'cyl1 = ', cyl[0]
print 'cyl2 = ', cyl[1]