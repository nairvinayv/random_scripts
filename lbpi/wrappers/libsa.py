#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python wrapper for libsa
Created on Wed Mar 29 11:53:15 2017

@author: nabina

"""
#import subprocess as sb
import sys
import re
import subprocess as sb
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as pl

import decimal


dirr = sys.argv[1]
lib_path = sys.argv[2]
flags = sys.argv[3]
energy_steps = sys.argv[4]
percentchange = sys.argv[5]
aux_peak = sys.argv[6]
cutoff = sys.argv[7]


    


shellpath = '/home/nabina/softwares/mgltools_x86_64Linux2_1.5.6/bin/pythonsh'
pythonpath = '/home/nabina/softwares/mgltools_x86_64Linux2_1.5.6/MGLToolsPckgs/AutoDockTools/Utilities24/'

def libsa():   
    
    libsa_run = sb.Popen([lib_path,'-ligand','{}ligand_protein.pdb'.format(dirr),\
    '-receptor','{}receptor.pdb'.format(dirr),flags, energy_steps, '1000', percentchange,\
    aux_peak, cutoff],stdout = sb.PIPE)  
                
    libsa_read = libsa_run.stdout.readlines()
    
    

#    if flags == 'none':
#        hist_dat = '{}nofilters_hist.dat'.format(dirr)
#        hist_png = '{}contactspectrum_wo_filter.png'.format(dirr)
#        spec_dat = '{}affinity_spectrumwofilter.dat'.format(dirr)     
#        filt_png = '{}affinityspectrum_wo_filter.png'.format(dirr)         
    
    if flags == 'affinity_only':
        hist_dat = '{}affinity_hist.dat'.format(dirr)
        hist_png = '{}affinity_hist.png'.format(dirr)
        spec_dat = '{}affinity_spectrum.dat'.format(dirr)    
        filt_dat = '{}affinity_filtering.dat'.format(dirr)    
        filt_png = '{}affinity_filtering.png'.format(dirr)                        
    
    if flags == 'fourier_only':
        hist_dat = '{}fourier_hist.dat'.format(dirr)
        hist_png = '{}fourier_hist.png'.format(dirr)
        
    if flags == 'affinity_fourier':
        hist_dat = '{}affinity_fourier_hist.dat'.format(dirr)
        hist_png = '{}affinity_fourier_hist.png'.format(dirr)    
        spec_dat = '{}affinity_spectrum_both.dat'.format(dirr)    
        filt_dat = '{}affinity_filtering_both.dat'.format(dirr)    
        filt_png = '{}affinity_filtering_both.png'.format(dirr)     
    

    with open(hist_dat,'w') as opn:
        for line in libsa_read:
            if re.match(b'MAIN:HIST', line):
                fields = line.split()
                opn.write('{:6}{:10}'.format(fields[1].decode('utf-8'), fields[2].decode('utf-8')))
                opn.write('\n')            
    opn.close()    
    
    data = np.loadtxt(hist_dat)
    xdata = data[:,0]
    ydata = data[:,1]    
    pl.xlabel("Residue ID")
    pl.ylabel("Normalized contact frequency")
    pl.plot(xdata,ydata,color='black',alpha=0.7, lw = 1)    
    
#    if flags == 'none':
#        pl.fill_between(xdata,ydata, color = 'brown')
#        pl.title("Contact histogram without filter\n")    
    
    if flags == 'affinity_only':
        pl.fill_between(xdata,ydata, color = 'orange')
        pl.title("Contact histogram after affinity filter \n")                         
    
    if flags == 'fourier_only':
        pl.fill_between(xdata,ydata, color = 'red')    
        pl.title("Contact histogram after high pass filter \n")  
        
    if flags == 'affinity_fourier':
        pl.fill_between(xdata,ydata, color = 'green')    
        pl.title("Contact histogram after affinity and high-pass filter \n") 

    pl.savefig(hist_png)
    pl.close()
    
    
    def affinity():
        #########    Preparation of histograms for affinity spectrum      ############    
   
        with open(spec_dat,'w') as opn:
            for line in libsa_read:
                if re.match(b'PLOT', line):
                    fields = line.split()
                    opn.write('{:15}{:15}'.format(fields[1].decode('utf-8'), fields[2].decode('utf-8')))
                    opn.write('\n')
        opn.close()
        
# this is the start of the normalization of the frequency of occurrence of affinity   
        lists0 = []; lists1 = [];
        aff_spec = open(spec_dat,'r').readlines()
        for line in aff_spec:
            ll = line.split()
            lists0.append(ll[0])
            lists1.append(int(ll[1]))
        print(lists1)
                
        max_val = max(lists1)
        with open(spec_dat,'w') as ff:
            for i in range(len(lists1)):
                ff.write('{:9}{:12}'.format(lists0[i],round(decimal.Decimal(lists1[i]/max_val),3)))
                ff.write('\n') 
        ff.close()
#-------------------------------------------------------------------------------
 
#        if flags != 'none':       
        with open(filt_dat,'w') as opn:
            for line in libsa_read:
                if re.match(b'REMARK:PEAK_INDEX_VALUE&MIN_MAX_ENERGY', line):
                    fields = line.split()
                    opn.write('{:12}{:12}'.format(fields[3].decode('utf-8'), fields[2].decode('utf-8')))
                    opn.write('\n')
        opn.close()
        
# this is the start of the normalization of the frequency of occurrence of affinity           
        lists0 = []; lists1 = [];
        aff_spec = open(filt_dat,'r').readlines()
        for line in aff_spec:
            ll = line.split()
            lists0.append(ll[0])
            lists1.append(int(ll[1]))

                
        max_val = max(lists1)
        with open(filt_dat,'w') as ff:
            for i in range(len(lists1)):
                ff.write('{:9}{:12}'.format(lists0[i],round(decimal.Decimal(lists1[i]/max_val),3)))
                ff.write('\n')   
        ff.close()
#-------------------------------------------------------------------------------            
        
    
        affinity_res=[]
        file = open(spec_dat,'r').readlines()
        for line in file:
            ff = line.split()
            if ff[1]!='0.000':
                affinity_res.append(float(ff[0]))
                
        print(min(affinity_res), max(affinity_res))
        data = np.loadtxt(spec_dat)
        xdata = data[:,0]
        ydata = data[:,1] 
        pl.bar(xdata,ydata,width=0.05,facecolor='lightblue',alpha=1)
#        pl.axis([(float(max(affinity_res))-1),(float(min(affinity_res))+1),0,max(ydata)])
        
       
        data = np.loadtxt(filt_dat)
        xdata = data[:,0]
        ydata = data[:,1] 
        pl.bar(xdata,ydata,width=0.05,facecolor='blue',alpha=1)
        pl.axis([(float(max(affinity_res))+0.5),(float(min(affinity_res))-0.5),0,max(ydata)])            
        
        pl.xlabel("Energy value (kcal/mol)")
        pl.ylabel("Number of occurence")
        pl.title("Affinity histogram \n")

        pl.savefig(filt_png)  
        pl.close() 
        
    if flags != 'fourier_only':
        affinity()
#    if flags != 'none':
#        affinity()
            

if __name__ == '__main__':  
    libsa()      











   