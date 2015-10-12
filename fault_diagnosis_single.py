# -*- coding: utf-8 -*-
"""
Created on Thu Oct 01 11:33:04 2015
@author: dimitris lourandos
"""
###############################################################################
#------------------------FUNCTIONS USED---------------------------------------#
###############################################################################

# a try to use numpy arrays for operations to increase speed

import numpy as np
import matplotlib.pyplot as plt
#import matplotlib.dates as mdates
from lourandos import *

cases = [180] # exclude zeros
lim_main  = 4
lim_suppl = 1 
filename1 = 'main_faults_some.csv'
filename2 = 'all_reports_input_new.csv'
na = '100' # number representing a symptom that is not available

###############################################################################
#-----------------------GETTING INITIAL DATA FROM FILES-----------------------#
###############################################################################

#read and store the FAULTS csv
row_count, fulltable = create_table(filename1)
fault_symptom = [x[1:len(x)] for x in fulltable[1:row_count]]
fault_symptom = np.array([ map(float,x) for x in fault_symptom ])


#Sort fulltable by possibility (use possibilty column, no.9)
#fault_symptom.sort(reverse = True, key = lambda x: float(x[9]))

# Separate main and supplemetary parameters in 2 different lists (tables)
fault_symptom_main = [fault_symptom[i][0:10] for i in range(row_count-1)]
fault_symptom_suppl = [fault_symptom[i][10:len(fault_symptom[0])-1] for i in range(row_count-1)]

# Store the engine's parameters(symptoms) in a list
parameters = fulltable[0]
parameters_main = fulltable[0][1:9]
parameters_suppl = fulltable[0][10:]
# Store the engine's possible faults in a list
faults = [fulltable[i][0] for i in range(1, row_count)]
possibilities = [fulltable[i][9] for i in range(1, row_count)]
critical_indeces = [int(fulltable[i][-1]) for i in range(1, row_count)]
#read and store the MEASUREMENTS csv
try: cases
except NameError: cases = None

row_count2, fulltable2 = create_table(filename2)
if cases is None:
    pass
else:
    cases.insert(0,0)
    fulltable2 = [fulltable2[i] for i in cases]
    row_count2 = len(cases)
    
vessel_name = []; date = [];
meas_main = [0]*(row_count2-1); meas_suppl = [0]*(row_count2-1);
for i in range (1, row_count2):    
    vessel_name.append(fulltable2[i][0]) # Store vessel's name in a list
    date.append(fulltable2[i][1])        # Store the report date in a list
    meas_main[i-1] = fulltable2[i][2:10] # Store the main parameters of the measurements in a list
    meas_suppl[i-1] = fulltable2[i][11:len(fulltable2[i])+1] # Store the supplementary parameters of the measurements in a list

#(vessel_name, date) = map(list, zip(*[(fulltable2[i][0], fulltable2[i][1]) for i in range (1, row_count2)]))

###############################################################################
#-----------CHECK FOR ERRONEOUS MEASUREMENTS or FAULTY SENSORS----------------#
###############################################################################

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
for i, meas in enumerate(meas_main):
    for j, symptom in enumerate(meas):
        check_meas(parameters_main[j], symptom)
    print



for i, meas in enumerate(meas_main):
    # 1. Pscav 
    if meas[1] !='0' and meas[3] !='0' and meas[5] == '0':  
        print '{}_Check Pscav measurement'.format(i)
#        cc[i] = 'Check Pscav measurement'
    # 2. BSFC
    if meas[6] ==-1 and all([I == '0' for n, I in enumerate(meas) if n!=6]):
        print '{}_Check Fuel Consumption or Power measurement'.format(i)
#        bc[i] = 'Low BSFC - Please check Fuel Consumption or Power measurement'
    if meas[6] == 1 and all([I == '0' for n, I in enumerate(meas) if n!=6]):
        print 'High BSFC - Please check Power or Fuel Consumption Measurement'
    # 3. TDC Correction
    if meas[4] ==0 and meas[5] ==0 and meas_suppl[i][-1] !=0:
#        tdc[i] = 'Check TDC correction'
        print '{}_Check indicator diagram for TDC correction'.format(i) #i, tdc[i] 
    # 4. TC speed
    if meas[2] !=0 and all([I == '0' for n, I in enumerate(meas) if n!=2]):
        print "{}_Check Turbocharger Speed measurement".format(i)
#    # 5. Torsion Meter
#    if meas_suppl[i][20] != 0 and all([I == '0' for I in meas]):
#	print 'Please check Torsion Meter reading' 
    # 6. Pscav, Pexh - This has to be done on HC level (absolute numbers not 1's and 0's)
#    if meas[1] - meas_suppl[i][1] < 0:
#        print 'Exete metrisei malakies'
#    elif meas[1] - meas_suppl[i][1] < 0.1:
#        print 'Small Pscav - Pexh difference - Pls check both measurements' 
#    elif meas[1] - meas_suppl[i][1] > 0.4:
#        print 'Very large Pscav - Pexh difference - Pls check both measurements'         
#    print
    
















###############################################################################
#-------------------------MAIN BODY OF THE PROGRAM----------------------------#
###############################################################################

# 1st part - Compare Main Symptoms
i=-1; bc = ['']*len(vessel_name); cc = ['']*len(vessel_name);
tdc = ['']*len(vessel_name); c_save = ['']*len(faults);
c2_save = [];
main_faults = ['0']*len(meas_main)
fault_counter = ['0']*len(meas_main)

for meas in meas_main: # check every case (report, measurement) -> meas = list
    i +=1
    main_faults_in = list(); fault_counter_in = list()
    c_save = ['']*len(faults)
    for fault_i in range(len(fault_symptom_main)):
        c = 0 #counter 
        for symptom_i in range(1, len(fault_symptom_main[fault_i])-1):
#            print symptom_i
            if meas[symptom_i-1] == fault_symptom_main[fault_i][symptom_i] or\
            meas[symptom_i-1] == na:
                c += 1
        if c >= lim_main:
            main_faults_in.append(fault_symptom_main[fault_i])
            fault_counter_in.append(fault_i)
        c_save[fault_i] = int(c)
    c2_save.append(c_save)
#   print c_save
    main_faults[i] = main_faults_in # this needs to be revisited
    fault_counter[i] = fault_counter_in # this provides right results
# Final check to ensure if something specific is going on,
# e.g. measurement fault or if there are inconsistencies in thermodynamic parameters
#    print i    

# Sort the main faults according to most matched parameters
# main_faults.sort(reverse = True, key = lambda x: int(x[10]))

# 2nd part - Compare Supplementary Symptoms    
ii=-1; ac = ['']*len(vessel_name); cc2_save = [];
main_faults2 = ['0']*len(meas_suppl)
fault_counter2 = ['0']*len(meas_suppl) 
for mn in range(len(meas_suppl)):
    ii+=1
    final_faults_in = list(); final_fault_counter = list()
    cc_save = [0]*len(faults)  
    if meas_suppl[mn][2] == '1':
#        print '{}.AC is fouled'.format(ii)
        ac[ii] = 'AC is fouled'
    elif meas_suppl[mn][2] =='-1':
#        print 'Check Air Cooler Pressure Drop measurement'
        ac[ii] = 'Check Air Cooler Pressure Drop measurement'
    for iii in fault_counter[mn]:
        c = 0 #counter
        for i in range (len(meas_suppl[0])):
            #print 'k =', k
            if meas_suppl[mn][i] == fault_symptom_suppl[iii][i]:
                c +=1
        if c >= lim_suppl:
            final_faults_in.append(faults[iii])
            final_fault_counter.append(iii)
        cc_save[iii] = c
    cc2_save.append(cc_save)
#    print    
#    print cc_save
    #print ii, vessel_name[ii], date[ii], final_faults_in        
    main_faults2[ii] = final_faults_in
    fault_counter2[ii] = final_fault_counter # this is right as well
cc_save = [(0 if x is "" else x) for x in cc_save]

c_all3 = list(np.array(c2_save)+np.array(cc2_save))
c_all3 = [list(x) for x in c_all3]

# Those do not work for adittion of list of lists
#c_all = [sum(x) for x in zip(cc2_save, c2_save)]
#from operator import add
#c_all2 = map(add, c2_save, cc2_save)


# Print no of report, fault, overall occurences of fault, 
ok_idx = ['']*len(fault_counter2) 
for n, f in enumerate(fault_counter2):
    ok_idex = ['']*len(faults)    
    for i in f:
#        print i
        if  meas_main[n][critical_indeces[i]-1] == fault_symptom[i][critical_indeces[i]]:
            ok_idex[i] = 'OK'
#    print n, faults[i], c_all3[n][i], ok_idex[0]
    ok_idx[n]=ok_idex


        
        
  
###############################################################################
#-------------------------WRITE RESULTS TO FILES------------------------------#
###############################################################################    

#with open('data_final.txt','w') as f:
#    for ii in range(0, len(date)):
#        val = str(ii+1) +'\t'+ vessel_name[ii] +'\t'+ date[ii] +'\t'+ str(fault_counter2[ii]) +'\t'+ str(main_faults2[ii]) +'\n'
#        f.write(val)
#    f.close()
#
# Preferable option 
# 
#with open('data_final2.csv','w') as f:
#    f.write('a/a; vessel name; date; fault_id; \n')
#    for ii in range(0, len(date)):
#        val = str(ii+1) +';'+ vessel_name[ii] +';'+ date[ii]+';'
#        f.write(val)        
#        for item in fault_counter2[ii]:
#            #print ii, item
#            f.write(str(item)+';')
#        f.write('\n')
#    f.close()

#with open('final_data.csv', 'w') as f:
#    for n, ss in enumerate(fault_counter2):
#        for i in ss:
#            val = str(n)+';'+faults[i]+';'+str(c_all3[n][i])+';'+ ok_idx[n][i]+';'+possibilities[i]+'\n'
#            f.write(val)
#    f.close()

###############################################################################
#-------------------------POST-PROCESSING OF DATA-----------------------------#
###############################################################################

# 1. Find how many reports correpond to each vessel
# 2. Find which fault appears most times in every vessel

Vnames = list(set(vessel_name)) #--> extract unique values from list as a list of a set
# or use the following to do the same:
#import collections
#Vnames = [i for i, count in collections.Counter(vessel_name).items() if count > 1]

vn = vessel_name[0]; vessel_d = [0]*len(Vnames);
vessel_nn = [0]*len(Vnames); vessel_f = [0]*len(Vnames);
vessel_n = []; vessel_date = []; vessel_fault = [];
nn = 0;

for i, vname in enumerate(vessel_name):
    if  vname == vn:
        vessel_n.append(vessel_name[i])
        vessel_date.append(date[i])
        vessel_fault.append(fault_counter2[i])
    else:
        vn = vname        
        vessel_d[nn] = vessel_date
        vessel_f[nn] = vessel_fault
        vessel_nn[nn] = vessel_n
        vessel_n = []; vessel_date = []; vessel_fault = [];
        vessel_n.append(vessel_name[i])
        vessel_date.append(date[i])
        vessel_fault.append(fault_counter2[i])      
        nn +=1
# Store the results of the last iteration in the lists
vessel_d[nn] = vessel_date
vessel_f[nn] = vessel_fault
vessel_nn[nn] = vessel_n

# check that all reports are stored in the above lists 
#sum_of_reports = 0
#for i in range(len(vessel_d)):
#    sum_of_reports += len(vessel_d[i])
#print sum_of_reports


# Store faults in lists per vessel

fault_occurence_per_vessel=[0]*len(vessel_f)
for v in range(0, len(vessel_f)): 
    c = 0; tt = [0]*len(fault_symptom)
    for i in range (0, len(fault_symptom)):
        for j in range(0, len(vessel_f[v])):
            if i in vessel_f[v][j]:
                c +=1
        #print i, counter
        tt[i] = c  
        c = 0 # counter
    fault_occurence_per_vessel[v] = tt 

# Faults as 0's and 1's per vessel per report
vessel = [0]*len(vessel_f); rr = [];
for v in range(len(vessel_f)):
    report = [0]*len(vessel_f[v])
    for r in range(len(vessel_f[v])):
        fault_per_report = [0]*len(faults)    
        for i in range(len(faults)):
            if i in vessel_f[v][r]:
                fault_per_report[i] = 1
            else:
                fault_per_report[i] = 0
        report[r] = fault_per_report
        rr.append(fault_per_report)
    vessel[v] = report

# Replace ACES with their Occurences, c
for i in range(len(rr)):
    for x in range(len(rr[i])):
        if rr[i][x] == 1:
            rr[i][x] = c_all3[i][x]

#ccc = np.array(c_all3)
#rr = np.array(rr)
#ccc = ccc[rr.astype(bool)]
##############
# WRITE TO FILE WITH FAULTS AS 0's AND 1's 
s=0
from os import path
filename = 'Results_for_main-{}_suppl-{}_Theodora'.format(lim_main, lim_suppl)
folderpath = path.relpath('G:/Documents/GitHub/Fault_diagnosis/Results/'+filename+'.csv')

with open(folderpath,'w') as f:
    f.write('These are the results for lim_main =%d & lim_suppl = %d \n' % (lim_main, lim_suppl))    
    f.write('a/a; vessel name; date;')
    for i in range(len(faults)):
        f.write(str(i)+';')
    f.write('\n')
    for i in range(len(vessel)):
        for j in range(len(vessel[i])):
            val = str(s+1) +';'+ vessel_name[s] +';'+ date[s]+';'
            f.write(val)        
            s +=1            
            for item in vessel[i][j]:
                f.write(str(item)+';')
            f.write(ac[s-1]+';'+bc[s-1]+'\n')
            #print ac[s-1]
    f.close()

# Faults as 0's and 1's per vessel per fault  
vessel2 = [0]*len(vessel_f)
for v in range(len(vessel_f)):
    fault_per_date = [0]*len(faults) 
    for i in range(len(faults)):
        report_faults = [0]*len(vessel_f[v])        
        for r in range(len(vessel_f[v])):
            if i in vessel_f[v][r]:
                report_faults[r] = 1
            else:
                report_faults[r] = 0
        fault_per_date[i] = report_faults    
    vessel2[v] = fault_per_date
 
# Convert date strings to numbers so as to plot them              
from datetime import datetime

def date2num(date):
    dates = datetime.strptime(date, '%Y-%m-%d')
    return dates.toordinal()

vessel_d_NUM = [0]*(len(vessel_d))
for i in range(len(vessel_d)):
    vessel_dnum = [0]*len(vessel_d[i])    
    for j in range(len(vessel_d[i])):
        d = date2num(vessel_d[i][j])
#        print vessel_d[i][j], d
        vessel_dnum[j] = d
    vessel_d_NUM[i] = vessel_dnum


###############################################################################
#-------------------------PLOTTING OF DATA------------------------------------#
###############################################################################

def bar_subplot(i, vnam_i, xlim, ylim):
    v_i = fig.add_subplot(3,3,i)
    v_i.bar(range(len(fault_symptom)), fault_occurence_per_vessel[i], align = 'center')
    v_i.set_ylim([0,ylim])
    v_i.set_xlim([0,xlim])
    v_i.set_xticks(range(11))
    v_i.set_title(vnam_i)
    v_i.yaxis.grid(True)
    
    
def bar_subplot2(i, vnam_i, xlim, ylim):
    v_i = fig.add_subplot(3,3,i)
    v_i.bar(range(len(fault_symptom)), [float(x)/len(vessel[i])*100 for x in fault_occurence_per_vessel[i]], align = 'center')
    v_i.set_ylim([0,ylim])
    v_i.set_xlim([0,xlim])
    v_i.set_xticks(range(len(fault_symptom)+1))
    v_i.set_title(vnam_i)
    v_i.yaxis.grid(True)

plt.ioff() # so as not to show the plot after run
fig = plt.figure(figsize = (17,11))
fig.suptitle(('Plot for lim_main =%d & lim_suppl = %d' % (lim_main, lim_suppl)), fontsize =18)
for i in range(len(vessel_nn)):
    vnam_i = vessel_nn[i][0]
    bar_subplot2(i, vnam_i, len(faults), 100)
    
#plt.show()

filename2 = ('Faults_for_{}_{}_Theodora.pdf'.format(lim_main, lim_suppl))
folderpath2 = path.relpath('G:/Documents/GitHub/Fault_diagnosis/Figures/'+filename2)
plt.savefig(folderpath2, format = 'pdf')
plt.close() # so as not to consume memory
#dates = mdates.strpdate2num(vessel_date[0], %Y-%m-%d)
#plot_date(dates, fault2[8])


#ticks_font = font_manager.FontProperties(family='Helvetica', style='normal',
#    size=sizeOfFont, weight='normal', stretch='normal')
#from matplotlib import rc, font_manager

#i = 1
#fig = plt.figure(figsize = (17,11))
#fig.suptitle(('Fault "'"%s"'" of vessel %s' % (faults[i], vessel_nn[i][0])), fontsize =14)
#pl = fig.add_subplot(111)
##ticks_font = font_manager.FontProperties(size=7)
#pl.bar(vessel_d_NUM[1],vessel2[1][6])
#pl.set_xticks(vessel_d_NUM[1], vessel_d[1], rotation = 50)

#for label in plt.get_xticklabels():
#    label.set_fontproperties(ticks_font)

    
#for j in range(len(faults)):
#    figure(j)
#    plt.bar(vessel_d_NUM[i],vessel2[i][j], align = 'center')
#    plt.title(('Fault "'"%s"'" of vessel %s' % (faults[j], vessel_nn[i][0])), fontsize =14)
#    plt.xticks(vessel_d_NUM[i], vessel_d[i], rotation = 50)
#    plt.ylim([0,1])    
#    plt.yticks([])
#    plt.show()



























