#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python wrapper for libsa
Created on Wed Mar 29 11:53:15 2017

@author: nabina

"""
#import subprocess as sb
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as pl






dirr = sys.argv[1]
libsa_flag = sys.argv[2] # libsanone and libsa 
flags = sys.argv[3]



    


shellpath = '/home/nabina/softwares/mgltools_x86_64Linux2_1.5.6/bin/pythonsh'
pythonpath = '/home/nabina/softwares/mgltools_x86_64Linux2_1.5.6/MGLToolsPckgs/AutoDockTools/Utilities24/'


def libsa_none():
    
    
    

    if flags == 'none':
        hist_dat = '{}nofilters_hist.dat'.format(dirr)
        hist_png = '{}contactspectrum_wo_filter.png'.format(dirr)
      
        data = np.loadtxt(hist_dat)
        xdata = data[:,0]
        ydata = data[:,1]    
        pl.xlabel("Residue ID")
        pl.ylabel("Normalized contact frequency")
        pl.plot(xdata,ydata,color='black',alpha=0.7, lw = 1)    
        pl.fill_between(xdata,ydata, color = 'brown')
        pl.title("Contact histogram without filter\n")    
        pl.savefig(hist_png)
        pl.close()        
        
        
    
    if flags == 'affinity_only':
        spec_dat = '{}affinity_spectrumwofilter.dat'.format(dirr)    
        filt_png = '{}affinityspectrum_wo_filter.png'.format(dirr)                        
        affinity_res=[]
        file = open(spec_dat,'r').readlines()
        for line in file:
            ff = line.split()
            if ff[1]!='0.000':
                affinity_res.append(float(ff[0]))
        data = np.loadtxt(spec_dat)
        xdata = data[:,0]
        ydata = data[:,1] 
        pl.bar(xdata,ydata,width=0.05,facecolor='brown',alpha=1)
        pl.axis([(float(max(affinity_res))+0.5),(float(min(affinity_res))-0.5),0,max(ydata)])      
        pl.xlabel("Energy value (kcal/mol)")
        pl.ylabel("Number of occurence")
        pl.title("Affinity histogram without filter \n")
        pl.savefig(filt_png)  
        pl.close() 







def libsa():   
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
    

   
    data = np.loadtxt(hist_dat)
    xdata = data[:,0]
    ydata = data[:,1]    
    pl.xlabel("Residue ID")
    pl.ylabel("Normalized contact frequency")
    pl.plot(xdata,ydata,color='black',alpha=0.7, lw = 1)    
    
 
    
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


if __name__ == '__main__':  
    if libsa_flag == 'libsanone':
        libsa_none()    
    if libsa_flag == 'libsa':
        libsa()











   