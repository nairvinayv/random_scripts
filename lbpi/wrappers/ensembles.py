#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 26 09:14:50 2017

for ensembles and includes:
multiple folders for ensembles
average histograms from each folders
histograms for LIBsa without filters
histograms for LIBsa with filters


if script_flags == 'folderplace':folders_target()
if script_flags == 'avghist':average_hist()        
if script_flags == 'libsanone': libsa_none()    
if script_flags == 'libsa':libsa()  
        
        
@author: nabina
"""




import os, re
import shutil
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as pl


dirr = sys.argv[1] # this should be the path for a common folder from forms
script_flags = sys.argv[2] # this flag is for running script function
 
###############################################################################


def folders_target():
    """
    Make multiple target folders for receptor
    
    """
    
    if not os.path.exists('{}/ensembles'.format(dirr)):
        os.path.join(os.mkdir('{}/ensembles'.format(dirr)))
        
    elif os.path.exists('{}/ensembles'.format(dirr)):    
        dirr
        
        
        
    source = '{}/protein/protein.pdb'.format(dirr)
    dest = '{}/ensembles/folder{}'.format(dirr, len(os.listdir('{}/ensembles'.format(dirr))))
    os.mkdir(os.path.join(dest))
    shutil.move(source, dest)


###############################################################################


def average_hist():
    
    """
    This function is to calculate an average of contact histograms and make a 
    single histograms for protein residues
    
    """
    
    module = sys.argv[3]  # this module is the flag for libsa modules like affinity or filter or both
    numpy_key = sys.argv[4]
  
    if module == 'file1': infile = 'nofilters_hist.dat'
    if module == 'file2': infile = 'affinity_spectrumwofilter.dat'    
    if module == 'file3': infile = 'affinity_hist.dat'    
    if module == 'file4': infile = 'affinity_spectrum.dat'    
    if module == 'file5': infile = 'affinity_filtering.dat'    
    if module == 'file6': infile = 'fourier_hist.dat'    
    if module == 'file7': infile = 'affinity_fourier_hist.dat'    
    if module == 'file8': infile = 'affinity_spectrum_both.dat'    
    if module == 'file9': infile = 'affinity_filtering_both.dat'  

#    infile = 'hist.dat'
#    outfile = 'testout.dat'

    aname = {};hist = {}; line = {}; ll={}
    hist_lists = []; col=[];cc={};
    a_count = list(range(len(os.listdir('{}ensembles'.format(dirr)))))
    
    for i in range(len(a_count)):
        aname[(i)] = '{}ensembles/folder{}/{}'.format(dirr, a_count[i], infile)
        hist[(i)] = []  
        line[(i)] = 'line[{}]'.format(i)
        ll[(i)] = 'll[{}]'.format(i)
        cc[(i)] = []  

        
    filenames = list(aname.values())   
    for i in range(len(filenames)):
        for line[i] in open(filenames[i], 'r').readlines():
            ll[i] = line[i].split()
            hist[i].append(float(ll[i][1]))
            cc[i].append(float(ll[i][0]))            
        hist_lists.append(hist[i])
        col.append(cc[i])
    
    
        
    data = np.array(hist_lists)
    length = np.array([len(i) for i in data])    # Get lengths of each row of data
    prepare = np.arange(length.max()) < length[:,None]    # Mask of valid places in each row
    # Setup output array and put elements from data into masked positions
    out = np.zeros(prepare.shape, dtype=data.dtype)
    out[prepare] = np.concatenate(data)
    numpy_sum = np.sum(out, axis=0)
    numpy_avg = numpy_sum/(len(filenames))
    histo_val = numpy_avg.tolist()

    
    
    if numpy_key == 'hist':
        with open('{}{}'.format(dirr, infile), 'w') as ff:
            for num, i in enumerate(histo_val):
                ff.write('{:8}{:15}'.format(str(num+1), str(i)))           
                ff.write('\n')
        ff.close()
        
        
    if numpy_key == 'aff':
        data = np.array(col)
        length = np.array([len(i) for i in data])    # Get lengths of each row of data
        prepare = np.arange(length.max()) < length[:,None]    # Mask of valid places in each row
        # Setup output array and put elements from data into masked positions
        out = np.zeros(prepare.shape, dtype=data.dtype)
        out[prepare] = np.concatenate(data)        
        numpy_sum1 = np.sum(out, axis=0)
        numpy_avg1 = numpy_sum1/(len(filenames))
        histo_val1 = numpy_avg1.tolist()
        with open('{}{}'.format(dirr, infile), 'w') as ff:
            for i in range(len(histo_val)):
#                print(histo_val1[i], histo_val[i])
                ff.write('{:20}{:20}'.format("%.8f" % histo_val1[i], "%.3f" %histo_val[i]))        
                ff.write('\n')
        ff.close()        


    
###############################################################################
    
    
    
def libsa_none():
    
    flags = sys.argv[3]    
    

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



###############################################################################




def libsa():   
    
    flags = sys.argv[3]    
    
    
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
    
###############################################################################
    
    def affinity():
        #########    Preparation of histograms for affinity spectrum      ############    

        affinity_res=[]
        file = open(spec_dat,'r').readlines()
        for line in file:
            ff = line.split()
            if ff[1]!='0.000':
                affinity_res.append(float(ff[0]))
                
#        print(min(affinity_res), max(affinity_res))
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




###############################################################################
def atoms_compare():
    """
    This function is to check if two uploaded files have same number of atoms
    to mention it as conformations of same ensembles
    
    """
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    
    #recep_com = '4epw.pdb'
    atoms1 = []; 
    atoms2 = []; 
    
             
    recep_file1 = open(file1,'r').readlines()
    for line in recep_file1:
        if re.match('ATOM',line[0:6]):atoms1.append(int(line[7:11]))   
        if re.match('HETATM',line[0:6]):atoms1.append(int(line[7:11]))       
    print('The number of atoms in {} is {}'.format(file1, len(atoms1)))
    
    
    
    recep_file2 = open(file2,'r').readlines()
    for line in recep_file2:
        if re.match('ATOM',line[0:6]):atoms2.append(int(line[7:11]))   
        if re.match('HETATM',line[0:6]):atoms2.append(int(line[7:11]))       
    print('The number of atoms in {} is {}'.format(file2, len(atoms2)))
    
    if len(atoms1) == len(atoms2):
        print('Same to Same hun')
    else: 
        print('ERROR !!!!!')

###############################################################################

    
if __name__ == '__main__':  
    if script_flags == 'folderplace':
        folders_target()
    if script_flags == 'avghist':
        average_hist()        
    if script_flags == 'libsanone':
        libsa_none()    
    if script_flags == 'libsa':
        libsa()    
    
    
    
    
