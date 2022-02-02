#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This file is for the calculation of the size of the grid box from the calculated 
size of the protein.

Created on Tue Mar 28 12:37:50 2017

@author: nabina
"""
import re
import sys
import decimal


receptor_path = sys.argv[1]
points = sys.argv[2]


def gridbox_size():
    maxval=[];
    file2 = open(receptor_path ,'r').readlines()
    
    
    x = []; y = []; z = [];
    for line in file2:        
        ff = line.split()
        if re.match('ATOM',line):
            x.append(float(ff[6]))
            y.append(float(ff[7]))
            z.append(float(ff[8]))
            
    xdist = round(decimal.Decimal((max(x)-min(x))+10),0)
    ydist = round(decimal.Decimal((max(y)-min(y))+10),0)
    zdist = round(decimal.Decimal((max(z)-min(z))+10),0)     
    max_val = max(xdist, ydist, zdist)
    maxval.append(max_val)
    
    best_spacing = round(max_val/126, 3)
    if best_spacing > 1: best_spacing = 1
        
    print("SPACING {}".format(best_spacing))  

 
    if points != 'none':
        ag1 = float(points) 
# calculation of number of points from the spacing value provided by user..         
        for i in maxval:            
            ag2=round(decimal.Decimal(float(i)/float(ag1))) 
            print('The value of npoints calculated becomes {}'.format(ag2))
            if ag2 <= 126:
                ag2 = ag2
            elif ag2 > 126:
                ag2 = 126
                print(' The value of npoints after conditions is {}'.format(ag2))
            
            if ag2 % 2 != 0:
                ag2 = ag2+1        
                
            ag2 = str(ag2)
            print('POINTS {}'.format(ag2))        





    

if __name__ == '__main__':  
    gridbox_size()   
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    