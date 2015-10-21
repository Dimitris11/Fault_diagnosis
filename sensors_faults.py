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
# 50 = Pcomp/Pscav
# 51 = TC speed/Pscav
# 52 = Pscav - Pexh

# Print symptoms
from lourandos import check_meas

print
j =4 # Column with -1, 0, 1
for i in [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 50, 51]:
    check_meas( parameters_all[i], HC_data[i,j] )
  
# Check for sensor faults/inconsistencies in measurements
  
print 'Now the sensor check starts:'
print  
# 1. Pscav 
if HC_data[19,j] !=0 and HC_data[16,j] ==0:
    print 'a. Check Scavenge Pressure measurement\
    b. Check Exhaust valve timing because of #1'

# 2. BSFC
if HC_data[12,j] !=0 and HC_data[17,j] ==0 and HC_data[23,j]==0 and \
HC_data[18,j] ==0 and HC_data[14,j] ==0:
    print 'Check Fuel Consumption or Power measurement because of #2'

# 3. TDC Correction
if HC_data[17,j] ==0 and HC_data[16,j] ==0 and HC_data[14,j] !=0:
    print 'a.Check pressure diagram measurement\
b. Sensor reading\
c. TDC correction procedure because of #3'
    
# 4. TC speed
if HC_data[18,j] !=0 and HC_data[23,j] ==0 and HC_data[19,j] ==0 and \
HC_data[17,j] ==0 and HC_data[14,j] ==0:
    print "Check Turbocharger Speed measurement because of #4"

# 5. Torsion Meter
if HC_data[15,j] !=0 and HC_data[23,j] ==0 and HC_data[19,j] ==0 and \
HC_data[17,j] ==0 and HC_data[16,j] ==0 and HC_data[14,j] ==0:
    print 'Please check Torsion Meter reading because of #5'

# 6. Exhaust Gas Temperature     
if HC_data[23,j] !=0 and HC_data[17,j] ==0 and HC_data[18,j] ==0 and \
HC_data[14,j] ==0:
    print 'Check for faulty exhaust receiver temperature\
    sensor because of #6'

#7. Texhaust & TC speed
if HC_data[23,j] ==1 and HC_data[18,j] ==-1:
    print 'Check for faulty exhaust receiver temperature sensor\
    and turbocharger speed measurement because if #7'
if HC_data[23,j] ==-1 and HC_data[18,j] ==1:
    print 'Check for faulty exhaust receiver temperature sensor\
    and turbocharger speed measurement because if #7'

#8. Scavenge pressure and TC speed
if HC_data[19,j] ==-1 and HC_data[18,j] == 1:
    print 'Check scavenge pressure because of #8'
if HC_data[19,j] == 1 and HC_data[18,j] ==-1:
    print 'Check scavenge pressure because of #8'
        
#9. Pscav - Pexh        
if HC_data[52,1] < 0.1 or HC_data[52,1] > 0.2:
    print "Check scavenge pressure or exhaust gas pressure because of #9"

#    if meas[1] - meas_suppl[i][1] < 0.1 or meas[1] - meas_suppl[i][1] > 0.3:
#        print 'Problem in Scavenge or Exhaust pressure measurement'
#    elif meas[1] - meas_suppl[i][1] < 0.1:
#        print 'Small Pscav - Pexh difference - Pls check both measurements' 
#    elif meas[1] - meas_suppl[i][1] > 0.4:
#        print 'Very large Pscav - Pexh difference - Pls check both measurements'         
#    print
