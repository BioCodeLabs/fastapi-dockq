from functions import pdock
import numpy as np
import Bio.PDB
from Bio.PDB import PDBParser
from schemes.payload import *

def calc_pdockq(path_file):
 
    chain_coords, chain_plddt = pdock.read_pdb(path_file)              
    t=8 
    if len(chain_coords.keys())<2 or len(chain_coords.keys())>2:
        print('Only one chain in pdbfile', chain_coords)
        payload=payloadScheme(pay_01="false",
        pay_02="ppv",pay_03="",pay_04="",pay_05="")
        return payload
    pdockq, ppv = pdock.calc_pdockq(chain_coords, chain_plddt, t)

    print('pDockQ =',np.round(pdockq,3),'for',path_file)
    print('This corresponds to a PPV of at least', ppv)
    filename=path_file.split("/")[1]
    probable_interaction= "yes" if pdockq>=0.23 else "no"

    payload=payloadScheme(pay_01=np.round(pdockq,3),
    pay_02=ppv,pay_03=probable_interaction,pay_04="",pay_05="")

    get_interacting_residues(path_file)
    return payload
    return f"pDockQ ={np.round(pdockq,3)} for {filename} \nThis corresponds to a PPV of at least, {ppv}.\t Interaction? {probable_interaction}"


def get_interacting_residues(path):
    
    residues=[]
    payload=payloadScheme(pay_01="",pay_02="",pay_03="",pay_04="",pay_05="")
    # create parser
    parser = PDBParser()

    # read structure from file
    structure = parser.get_structure('id',path)
    print("ge")
    chains = structure[0]

    if (len(chains)>2):
        return
    chains_model=[]
    for chain in chains:
        print(chain.get_id())
        chains_model.append(chain)

    print(len(chains))
    #chain = chains['A']
    #chain2 =  chains['B']

    chain = chains_model[0]
    chain2 =  chains_model[1]
    index_chain1=[]
    index_chain2=[]


    for residue1 in chain:
        for residue2 in chain2:
            if residue1 != residue2:
                try:
                    distance = residue1['CA'] - residue2['CA']
                except KeyError:
                    continue
                if distance < 8:
                    residue_in_interface=True
                    
                    if residue1.get_id()[1] not in index_chain1:
                        index_chain1.append(residue1.get_id()[1])
                    if residue2.get_id()[1] not in index_chain2:
                        index_chain2.append(residue2.get_id()[1])
                
                    min_distance=calc_min_dist(residue1,residue2)
                    payload = {
                        "pay_01":residue1.get_resname(),
                        "pay_02":residue1.get_id()[1],
                        "pay_03":residue2.get_resname(),
                        "pay_04":residue2.get_id()[1],
                        "pay_05":str(min_distance)

                    }

                    residues.append(payload)
                    print(residue1, residue2, distance)
                    


            # stop after first residue
            #break


    return residues    


def calc_min_dist(residue1, residue2):
    distances = []
    for atom1 in residue1:
        for atom2 in residue2:
            distances.append(atom1-atom2)
    return min(distances)