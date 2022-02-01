#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 12:37:50 2017

@author: nabina
"""
import re
import subprocess as sb
import sys


pdb_path = sys.argv[1]
chnatm_path = sys.argv[2]
protein_path = sys.argv[3]
protein_pdbqt = sys.argv[4]
receptor_path = sys.argv[5]


print("--------------------------")
print(sys.argv)
print("--------------------------")


#shellpath = '/home/fs/npaudyal/software/mgltools_x86_64Linux2_1.5.6/bin/pythonsh'
#pythonpath = '/home/fs/npaudyal/software/mgltools_x86_64Linux2_1.5.6/MGLToolsPckgs/AutoDockTools/Utilities24/'

#shellpath = '/home/nabina/MGLTools-1.5.6/bin/pythonsh'
#pythonpath = '/home/nabina/MGLTools-1.5.6/MGLToolsPckgs/AutoDockTools/Utilities24/'


shellpath = '/content/mgltools_x86_64Linux2_1.5.7/bin/pythonsh'
pythonpath = '/content/mgltools_x86_64Linux2_1.5.7/MGLToolsPckgs/AutoDockTools/Utilities24/'


def receptor_prepare():  

    res_lists = ['ALA', 'ARG', 'ASN', 'ASP', 'CYS', 'GLN', 'GLU', 'GLY', 'HIS',\
                 'ILE', 'LEU', 'LYS', 'MET', 'PHE', 'PRO', 'SER', 'THR', 'TRP',\
                 'TRS', 'TYR', 'VAL']

    chains = []; hetatmss = [];

    for line in open(chnatm_path,'r').readlines():
        if re.match('CHAINS', line):
            fields = line.split();chains.append(fields[1])          
        if re.match('HETATMS', line):
            fields = line.split();hetatmss.append(fields[1])    

    print(chains) 
    print(hetatmss)



## writing protein structure with selected hetatms
       
    in_file = open(pdb_path, 'r').readlines() 
    with open(protein_path,'w') as ff:
        for line in in_file:        
            for i in range(len(res_lists)): 
                if re.match('ATOM'+res_lists[i],line[0:4]+line[17:20]):
                    ff.write(line)
            for i in range(len(hetatmss)): 
                if re.match('HETATM'+hetatmss[i],line[0:6]+line[17:]):
                    ff.write('HETATM'+line[6:23]+'  1'+line[26:]) 
                if re.match('ATOM'+hetatmss[i],line[0:4]+line[17:]):
                    ff.write('HETATM'+line[6:23]+'  1'+line[26:])                     
    ff.close()
    
    

## writing protein structure only with selected chains and hetatms
  
    file = open(protein_path, 'r').readlines()
    with open(protein_path,'w') as p: 
        for line in file:   
            for i in range(len(chains)): 
                if re.match('ATOM'+chains[i],line[0:4]+line[21:22]):
                    p.write(line) 
                if re.match('HETATM'+chains[i],line[0:6]+line[21:22]):
                    p.write(line)                 
    p.close()

    
    resids = []
    dd = {}
     
    
    tt = open(protein_path, 'r').readlines()
    
    for i in chains:
        for line in tt:
            if re.match('ATOM'+'CA'+i, line[0:4]+line[13:15]+line[21:22]):            
                resids.append(line[21:26])
    #print(resids)
    
    
    for num, j in enumerate(resids):
        if len(str(num+1)) == 1:dd[(j)] = (str("   "+str(num+1)))
        if len(str(num+1)) == 2:dd[(j)] = (str("  "+str(num+1)))
        if len(str(num+1)) == 3:dd[(j)] = (str(" "+str(num+1)))   
        if len(str(num+1)) == 4:dd[(j)] = (str(num+1))   
    
    
    with open(protein_path, 'w') as pp:
        for line in tt:
            if re.match('ATOM', line[0:4]):    
                if line[21:26] in dd:
                    kk = dd[(line[21:26])]
                    pp.write(line[0:22]+kk+line[26:])
            if re.match('HETATM',line[0:6]):
                pp.write('ATOM  '+line[6:]) 
    pp.close()
    
    
    
    
    
    
###############################################################################
##### Formation of pdbqt files....    
    
    sb.call([shellpath, '{}prepare_receptor4.py'.format(pythonpath), '-r', protein_path, '-A', 'hydrogens', '-o', protein_pdbqt])
    print('\t\t------   Receptor preparation is complete  ------ \n')    
    
    file1 = open(protein_pdbqt,'r').readlines()
    with open(receptor_path,'w') as ff:
        ff.write("REMARK File originally originated from pdb file \n")
        for num,line in enumerate(file1):        
            if re.match('ATOM',line):
                old = (line[0:len(line)])
                new = (line[0:59]+'   0.00   '+'   U    '+line[77])
                a = line.replace(old,new)
                ff.write(a)
                ff.write('\n')
       
    ff.close()     
    


if __name__ == '__main__':  
    receptor_prepare()   
