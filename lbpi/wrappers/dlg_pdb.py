#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 12:26:43 2017

@author: nabina
"""

import sys
import re



dirr = sys.argv[1]
lib_path = sys.argv[2]
flags = sys.argv[3]
print('the flag is {}'.format(flags))


def dlg_pdb():   
    
    if flags == 'pdb':

        file = open('{}protein.pdb'.format(dirr),'r').readlines()
        with open('{}receptor.pdb'.format(dirr),'w') as ff:
            ff.write("REMARK File originally originated from pdb file \n")
            for num,line in enumerate(file):        
                if re.match('ATOM',line):
                    old = (line[0:len(line)])
                    new = (line[0:59]+'   0.00   '+'   U    '+line[77])
                    a = line.replace(old,new)
                    ff.write(a)
                    ff.write('\n')
           
        ff.close()             
        
        
    if flags == 'dlg':
        in_file = open('{}dock_dlg.dlg'.format(dirr), 'r').readlines() 
        with open('{}edited.pdb'.format(dirr),'w') as opn:
            for line in in_file:
                if re.match('DOCKED', line):               
                    opn.write(line[8:len(line)])            
        opn.close()
        
        
        file1 = open('{}edited.pdb'.format(dirr),'r').readlines()
        with open('{}ligand_protein.pdb'.format(dirr),'w') as ff:
            for num,line in enumerate(file1):
                if re.match('MODEL',line):
                    ff.write(line)
     
                if re.match('USER',line):
                    ff.write(line)
    
                if re.match('ATOM',line):
                    old = (line[0:len(line)])
                    new = (line[0:12]+' '+line[13]+'   '+'LIG'+'     1     '+line[31:66]+'           '+line[13]+'  ')
                    a = line.replace(old,new)
                    ff.write(a)
                    ff.write('\n')
    
    
                if re.match('ENDMDL',line):
                    ff.write(line)
    
        ff.close() 
    
    
    
    
            

if __name__ == '__main__':  
    dlg_pdb()      
