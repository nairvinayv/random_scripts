#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 26 09:14:50 2017

This script is for making sure two uploaded receptor conformations are of the 
same ensembles which will be used for the calculation of average SNR of multiple 
conformations

@author: nabina
"""


#import re
import sys,os
import subprocess as sb
import shutil


arg1 = sys.argv[1]   # flag arguments for defining the modules to be operated
arg2 = sys.argv[2]   # wrapper files
arg3 = sys.argv[3]   # working folder


def work_files():
    
    """
    This function is to find out the folders present in ensembles and prepare receptor 
    in each folders and also to copy ligands to each folders. Finally, depending 
    on the flag defined it helps in running autodock or LIBSA
   
    """
      
    pdb_path = '{}protein.pdb'.format(arg3)
    ligand_path = '{}ligand.pdbqt'.format(arg3)
    chnatm_path = '{}chnatm.dat'.format(arg3)
    protein_path = []
    protein_pdbqt = []
    receptor_path = []




    aname = {}; 
    a_count = list(range(len(os.listdir('{}ensembles'.format(arg3)))))
     
    for i in range(len(a_count)):aname[(i)] = '{}ensembles/folder{}/'.format(arg3, a_count[i])         
    dirr = list(aname.values())
    
    for i in range(len(dirr)):
        protein_path.append('{}protein.pdb'.format(dirr[i]))
        protein_pdbqt.append('{}protein.pdbqt'.format(dirr[i]))
        receptor_path.append('{}receptor.pdb'.format(dirr[i]))
        
        
    for i in range(len(dirr)):
        if arg1 == 'adt':  
            space = sys.argv[4]
            points = sys.argv[5]
            evals = sys.argv[6]  
            gens = sys.argv[7]  
            run = sys.argv[8]             
            sb.call(['python', '{}pdb_prepare.py'.format(arg2), pdb_path, chnatm_path, protein_path[i], protein_pdbqt[i], receptor_path[i]])        
            shutil.copy(ligand_path, dirr[i])  # copying of ligand_pdbqt to ensemble folders            
            sb.call(['python', '{}adt.py'.format(arg2), dirr[i], space, points, evals, gens, run]) 
            
            
            
        if arg1 == 'libsa_none':
            LIBSA = sys.argv[4]            
            sb.call(['python', '{}libsa_none.py'.format(arg2), dirr[i], LIBSA, 'none', '0.05','1','0.4','4'])  
            sb.call(['python', '{}libsa_none.py'.format(arg2), dirr[i], LIBSA, 'affinity_only', '0.05','1','0.4','4'])  
            
            
        if arg1 == 'libsa':
            LIBSA = sys.argv[4]            
            arg5 = sys.argv[5]
            arg6 = sys.argv[6]  
            arg7 = sys.argv[7]  
            arg8 = sys.argv[8]  
            arg9 = sys.argv[9]             
            sb.call(['python', '{}libsa.py'.format(arg2), dirr[i], LIBSA, arg5,arg6, arg7, arg8, arg9])  



    """
    Subprocess call for views file to automate adt and LIBSA for ensembles
    
    sb.call(['python', '{}adt_ens.py'.format(wrappers), 'adt', wrappers, current_dir, space, points, evals, gens, run]) 
    sb.call(['python', '{}adt_ens.py'.format(wrappers), 'libsa_none', wrappers, current_dir,LIBSA])  
    sb.call(['python', '{}adt_ens.py'.format(wrappers), 'libsa', wrappers, current_dir, LIBSA, libsa_flags, energy_steps, percentchange, aux_peak, cutoff]) 
   
    """

if __name__ == '__main__':  
    work_files() 




