#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python wrapper for autodock 
Created on Wed Mar 29 11:53:15 2017

@author: nabina

"""
import subprocess as sb
import sys
import re

dirr = sys.argv[1]
space = sys.argv[2]
points = sys.argv[3]  
evals = sys.argv[4]
gens = sys.argv[5]
run = sys.argv[6]

shellpath = '/home/nabina/softwares/mgltools_x86_64Linux2_1.5.6/bin/pythonsh'
pythonpath = '/home/nabina/softwares/mgltools_x86_64Linux2_1.5.6/MGLToolsPckgs/AutoDockTools/Utilities24/'


def adt():
    
    
    sb.call([shellpath, '{}prepare_gpf4.py'.format(pythonpath), '-l', '{}ligand.pdbqt'.format(dirr),\
    '-r', '{}protein.pdbqt'.format(dirr),'-p',points,'-p',space, '-o', '{}protein.gpf'.format(dirr) ])
    ag = sb.Popen(['/home/nabina/softwares/x86_64Linux2/autogrid4','-p','protein.gpf','-l','protein.glg'], cwd = dirr)
    ag.wait()
    
    
    sb.call([shellpath, '{}prepare_dpf4.py'.format(pythonpath), '-l', '{}ligand.pdbqt'.format(dirr),\
    '-r', '{}protein.pdbqt'.format(dirr),'-p',evals,'-p',gens,'-p',run, '-o', '{}ligand_protein.dpf'.format(dirr) ]) 
    ad = sb.Popen(['/home/nabina/softwares/x86_64Linux2/autodock4','-p','ligand_protein.dpf','-l','ligand_protein.dlg', '&'], cwd = dirr)
    ad.wait() 



    in_file = open('{}ligand_protein.dlg'.format(dirr), 'r').readlines() 
    with open('{}edited.pdb'.format(dirr),'w') as opn:
        for line in in_file:
            if re.match('DOCKED', line):               
                opn.write(line[8:len(line)])       
    opn.close()
    
    file1 = open('{}edited.pdb'.format(dirr),'r').readlines()
    with open('{}ligand_protein.pdb'.format(dirr),'w') as ff:
        for num,line in enumerate(file1):
            if re.match('MODEL',line):ff.write(line) 
            if re.match('USER',line):ff.write(line)
            if re.match('ATOM',line):
                old = (line[0:len(line)])
                new = (line[0:12]+' '+line[13]+'   '+'LIG'+'     1     '+line[31:66]+'           '+line[13]+'  ')
                a = line.replace(old,new)
                ff.write(a)
                ff.write('\n')
            if re.match('ENDMDL',line):ff.write(line)
    ff.close()         

if __name__ == '__main__':  
    adt()      


  
