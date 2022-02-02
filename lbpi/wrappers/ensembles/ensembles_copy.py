import os
import shutil
import sys

dirr = sys.argv[1] # this should be the path for a common folder from forms
flags = sys.argv[2]
print(dirr)


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



def ligand_copy():
    """
    Copy ligand file to each folder and set the folder ready
    
    """    
    
    folder_list = []
    for i in os.listdir('{}/ensembles'.format(dirr)):
        folder_list.append('{}/ensembles/{}/'.format(dirr, i))
    
    ligand_path = '{}/ligand.pdbqt'.format(dirr)

    for i in folder_list:
        shutil.copy(ligand_path, i)
        


if __name__ == '__main__':  
    if flags == 'folderplace':
        folders_target()
    elif flags == 'ligcopy':
        ligand_copy()





    
    
    
#folders_target()    
#ligand_copy()    















#source = 'source/test.dat'
#dest = 'dest/'
#os.mkdir('dest')
#
#shutil.move(source, dest)
