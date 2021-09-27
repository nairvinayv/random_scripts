# -*- coding: utf-8 -*-
"""
This file is for the extraction of the hetatms present in the pdb file either
ATOM list or HETATM list

Created on Mon Feb  6 13:17:28 2017

@author: npaudyal
"""

###############################################################################
##### command line coding for atom and hetatom list from updated pdbfile or 
##### downloaded pdb file
 


import re
import sys


recep_com = sys.argv[1]





def receptor_lists():               

    
    # list introduction
    res_lists = []; hetatms_list = []; chain = [];  

    
    # dictionary for residues and elements    
    res_dict = {'HIS':'HIS', 'ASP':'ASP', 'ARG':'ARG', 'PHE':'PHE', 'ALA':'ALA', 'CYS':'CYS', 'GLY':'GLY',\
                'GLN':'GLN', 'GLU':'GLU', 'LYS':'LYS', 'LEU':'LEU', 'MET':'MET', 'ASN':'ASN', 'SER':'SER',\
                'TYR':'TYR','THR':'THR','ILE':'ILE','TRP':'TRP','PRO':'PRO','VAL':'VAL'}
    

    # reading chains, hetatms from the pdb file     
    recep_file = open(recep_com,'r').readlines()
    for line in recep_file:
        if re.match('ATOM',line[0:6]):  
            res_lists.append(line[17:20])
            chain.append(line[21:22])
            

           
              
        if re.match('HETATM',line[0:6]):
            res_lists.append(line[17:20])
#            chain.append(line[21:22])
            
            
    print(sorted(set(res_lists)))   
                   
    for i in (sorted(set(res_lists))):
        if i not in res_dict:
            hetatms_list.append(i.strip())

          
 
 ### heteroatoms and chain present in the pdb file to be selected by the user...    
#    for i in hetatms_list:
#        if i == 'HOH':
#            hetatms_list.remove(i)
#        if len(i) < 3:
#            hetatms_list.remove(i)
#
#    for i in hetatms_list:
#        print('HETATM {}'.format(i))
#        
#    for i in sorted(set(chain)):
#        print('CHAIN {}'.format(i))

    hetatms_list = [a for a in hetatms_list if not a == 'HOH' and len(a) == 3]

    for i in hetatms_list:
        print('HETATM {}'.format(i))

        
    for i in sorted(set(chain)):
        print('CHAIN {}'.format(i))
  


if __name__ == '__main__':  
    receptor_lists()   
