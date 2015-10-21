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
#import matplotlib.pyplot as plt

#cases = range(240,245) # exclude zeros
limit  = 4
filename1 = 'main_faults_all.csv'
filename2 = 'Philippe_01_2007.csv'

###############################################################################
#-----------------------GETTING INITIAL DATA FROM FILES-----------------------#
###############################################################################

execfile('input_data_np.py')

###############################################################################
#-----------CHECK FOR ERRONEOUS MEASUREMENTS or FAULTY SENSORS----------------#
###############################################################################

execfile('sensors.py')

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
 

# Sort the main faults according to most matched parameters
# main_faults.sort(reverse = True, key = lambda x: int(x[10]))


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



























