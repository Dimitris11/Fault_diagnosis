#          MAIN PARAMETERS

# 0 = Exhaust Gas Temperature (Texh)
# 1 = Scavenge Pressure(Pscav)
# 2 = Turbocharger Speed (TC Speed)
# 3 = Pcomp/Pscav
# 4 = Maximum Pressure (Pmax)
# 5 = Compression Pressure (Pcomp)
# 6 = Brake Specific Fuel Consumption (BSFC)
# 7 = Pmax - Pcomp 

# Print symptoms
from lourandos import check_meas

print ''
#for i, meas in enumerate(meas_main):
#   for j, symptom in enumerate(meas):
#        check_meas(parameters_main[j], symptom)
#   print 

for i, meas in enumerate(meas_main):
#    c1=0
#    c2=0
#    c3=0
    # 1. Pscav 
    if meas[1] !='0' and meas[5] == '0':
#        c1 = c1 + 1
        print '{}_a. Check Scavenge Pressure measurement\
        b. Check Exhaust valve timing because of #1'.format(i)
#        cc[i] = 'Check Pscav measurement'
    # 2. BSFC
    if meas[6] !='0' and meas[4]=='0' and meas[0]=='0' and meas[2]=='0' and meas_suppl[i][7]=='0':
        print '{}_Check Fuel Consumption or Power measurement because of #2'.format(i)
#        bc[i] = 'Low BSFC - Please check Fuel Consumption or Power measurement'
#    if meas[6] == '1' and all([I == '0' for n, I in enumerate(meas) if n!=6]):
#        print '{}_High BSFC - Please check Power or Fuel Consumption Measurement'.format(i)
    # 3. TDC Correction
    if meas[4] =='0' and meas[5] =='0' and meas_suppl[i][7] !='0':
#        tdc[i] = 'Check TDC correction'
        print '{}_a.Check pressure diagram measurement\
        b. Sensor reading\
        c. TDC correction procedure because of #3'.format(i) #i, tdc[i] 
    # 4. TC speed
    if meas[2] !='0' and meas[0]=='0' and meas[1]=='0' and meas[4]=='0' and meas_suppl[i][7]=='0':
#        c2 = c2 + 1
        print "{}_Check Turbocharger Speed measurement because of #4".format(i)
#    # 5. Torsion Meter
    if meas_suppl[i][8] != '0' and meas[0]=='0' and meas[2]=='0' and meas[4]=='0' and meas[5]=='0' and meas_suppl[i][7]=='0':
        print '{}_Please check Torsion Meter reading because of #5'.format(i) 
    # _. Pscav, Pexh 
#    if meas[1] - meas_suppl[i][1] < 0.1 or meas[1] - meas_suppl[i][1] > 0.3:
#        print 'Problem in Scavenge or Exhaust pressure measurement'
#    elif meas[1] - meas_suppl[i][1] < 0.1:
#        print 'Small Pscav - Pexh difference - Pls check both measurements' 
#    elif meas[1] - meas_suppl[i][1] > 0.4:
#        print 'Very large Pscav - Pexh difference - Pls check both measurements'         
#    print
    # 6. Exhaust gas temperature (it can be an indication of many faults
    #    even if it is present alone, without any other symptoms)
    if meas[0] != '0' and meas[4]=='0' and meas[2]=='0' and meas_suppl[i][7]=='0':
#        c3 = c3 + 1
        print '{}_Check for faulty exhaust receiver temperature sensor because of #6'.format(i)
    #7. Texhaust & TC speed
    if meas[0]=='1' and meas[2]=='-1':
#        if c2==0 and c3==0:
            print '{}_Check for faulty exhaust receiver temperature sensor and turbocharger speed measurement because if #7'.format(i)
#        elif c2==1 and c3==0:
#            print '{}_Check for faulty exhaust receiver temperature sensor'.format(i)
#        elif c2==0 and c3 ==1:
#            print '{}_Check turbocharger speed measurement'.format(i)
    if meas[0]=='-1' and meas[2]=='1':
#        if c2==0 and c3==0:
            print '{}_Check for faulty exhaust receiver temperature sensor and turbocharger speed measurement because if #7'.format(i)
#        elif c2==1 and c3==0:
#            print '{}_Check for faulty exhaust receiver temperature sensor'.format(i)
#        elif c2==0 and c3 ==1:
#            print '{}_Check turbocharger speed measurement'.format(i)
    #8. Scavenge pressure and TC speed
    if meas[1]=='-1' and meas[2]=='1':
#        if c1==0:
            print '{}_Check scavenge pressure because of #8'.format(i)
    if meas[1]=='1' and meas[2]=='-1':
#        if c1==0:
            print '{}_Check scavenge pressure because of #8'.format(i)