import csv
from functions import pdock
import numpy as np
import Bio.PDB
from Bio.PDB import PDBParser
from schemes.payload import *
import uuid

def calc_pdockq(path_file):
 
    chain_coords, chain_plddt = pdock.read_pdb(path_file)              
    t=8 
    if len(chain_coords.keys())<2 or len(chain_coords.keys())>2:
        print('Only one chain in pdbfile', chain_coords)
        payload=payloadScheme(pay_01="false",
        pay_02="ppv",pay_03="",pay_04="",pay_05="",pay_06="",pay_07="",pay_08="",pay_09="",pay_10="")
        return payload
    pdockq, ppv = pdock.calc_pdockq(chain_coords, chain_plddt, t)

    print('pDockQ =',np.round(pdockq,3),'for',path_file)
    print('This corresponds to a PPV of at least', ppv)
    filename=path_file.split("/")[1]
    probable_interaction= "Yes" if pdockq>=0.23 else "No"
    payload=payloadScheme(pay_01=str(np.round(pdockq,3)),
    pay_02=ppv,pay_03=probable_interaction,pay_04="",pay_05="",pay_06="",pay_07="",pay_08="",pay_09="",pay_10="")
    get_interacting_residues(path_file)
    return payload


def get_interacting_residues(path):
    
    residues=[]
    payload=payloadScheme(pay_01="",pay_02="",pay_03="",pay_04="",pay_05="",pay_06="",pay_07="",pay_08="",pay_09="",pay_10="")
    parser = PDBParser()
    structure = parser.get_structure('id',path)
    chains = structure[0]

    if (len(chains)>2):
        return
    chains_model=[]
    for chain in chains:
        print(chain.get_id())
        chains_model.append(chain)

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
                        "pay_03":get_residue_bfactor(residue1),
                        "pay_04":residue2.get_resname(),
                        "pay_05":residue2.get_id()[1],
                        "pay_06":get_residue_bfactor(residue2),
                        "pay_07":str(min_distance),
                        "pay_08":"",
                        "pay_09":"",
                        "pay_10":"",
                        

                    }

                    residues.append(payload)
                    print(residue1, residue2, distance)
                
    return residues    


def calc_min_dist(residue1, residue2):
    distances = []
    for atom1 in residue1:
        for atom2 in residue2:
            distance=atom1-atom2
            distances.append(distance)
    return min(distances)

def get_csv_results(payload):
    unique_id = uuid.uuid4()
    unique_id_str = str(unique_id)
    reduced_id=unique_id_str[1:8]
    csv_heaver=['Residue1', 'Position1', 'Confidence1', 'Residue2','Position2','Confidence2','Distance']
    csv_data=[]
    print(csv_heaver)

    for item in payload:
        csv_data.append([item.pay_01,item.pay_02,item.pay_03,item.pay_04,item.pay_05,item.pay_06,item.pay_07])
    path=f'csv/{reduced_id}_residue_distances.csv'
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(csv_heaver)
        writer.writerows(csv_data)

    return path

def get_residue_bfactor(residue1):
    bfactors=[]
    for atom in residue1.get_atoms():
        bfactors.append(atom.get_bfactor())
    return max(bfactors)