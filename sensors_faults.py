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

#11. Shaft (FPI) vs Shaft from torsion meter
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
        
    
    
#eff_diff = HC_data[87,2]*100; shaft_diff = HC_data[15,4]
#if abs(eff_diff) <= 2:
##    pr = 'Mechanical efficiency is OK'
#    p =  0;
#elif eff_diff < 5. and eff_diff > 2.:
#    pr = 'Mechanical efficiency is HIGH'
#    p =  1; k+=1
#elif eff_diff > -5. and eff_diff < -2.:
#    pr = 'Mechanical efficiency is LOW'
#    p = -1; k+=1
#elif eff_diff < -5.:
#    pr = 'Mechanical efficiency is VERY LOW'
#    p = -2; k+=1
#elif eff_diff > 5.:
#    pr = 'Mechanical efficiency is VERY HIGH'
#    p =  2; k+=1
#else:
#    pr = 'Something went wrong with mechanical efficiency'
#
#try: print pr
#except NameError: print 
#
#  
#if p == 0:
#    if shaft_diff ==  0:
#        pr2 =  'Indicated and Shaft is OK'
#    if shaft_diff == -1:
#        pr2 =  'Indicated and Shaft is Low - check both measurements, possible fault'
#        k+=1
#    if shaft_diff ==  1:
#        pr2 =  'Indicated and Shaft are high - possible hull fouling'
#        k+=1
#elif p == 1:
#    if shaft_diff ==  0:
#        pr2 =  'Indicated Power is low - Check Measurement'
#    if shaft_diff ==  1:
#        pr2 =  'Indicated Power is OK, check Torsion Meter'    
#elif p == -1:
#    if shaft_diff == 1:
#        pr2 =  'Indicated is OK and Shaft is Low - check Torsion Meter'
#    if shaft_diff == 0:
#        pr2 =  'Indicated is high and Shaft is OK - check Indicated'
#elif p == 2:
#    if shaft_diff ==  1:
#        pr2 =  'Indicated is low and Shaft Power is high - check both'  
#elif p == -2:
#    if shaft_diff ==  1:
#        pr2 =  'Indicated is high and Shaft Power is low - check both'
#        
#try: print pr2+' because of #11'
#except NameError: print "No Fault"
    
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
    
