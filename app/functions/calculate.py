from functions import pdock
import numpy as np

def calc_pdockq(path_file):
 
    chain_coords, chain_plddt = pdock.read_pdb(path_file)              
    t=8 
    if len(chain_coords.keys())<2:
        print('Only one chain in pdbfile', chain_coords)
        return
    pdockq, ppv = pdock.calc_pdockq(chain_coords, chain_plddt, t)

    print('pDockQ =',np.round(pdockq,3),'for',path_file)
    print('This corresponds to a PPV of at least', ppv)
    filename=path_file.split("/")[1]
    probable_interaction= "yes" if pdockq>=0.23 else "no"

    return f"pDockQ ={np.round(pdockq,3)} for {filename} \nThis corresponds to a PPV of at least, {ppv}.\t Interaction? {probable_interaction}"
