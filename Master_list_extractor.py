import pandas as pd

UNI_ID = pd.read_csv("Uniprot_ids.csv")
UNI_ID = list(UNI_ID['Uniprot_ID'])

temp = pd.read_csv("UniProt_PubMed_mapping.csv")
UNI_PUBMED = temp.dropna()
print (len(UNI_PUBMED))
UNI_PDB = pd.read_csv("UniProt_PDB_mapping.csv")
print (len(UNI_PDB))

master_df = pd.DataFrame(columns = ['Uniprot_id','Pubmed_links','PDB_ids'])

for idx,uni_id in enumerate(UNI_ID):
    if(uni_id in list(UNI_PUBMED['Uniprot_ID'])):
        pubmed = UNI_PUBMED.loc[UNI_PUBMED['Uniprot_ID'] == uni_id, ['PubMed_ID']].iloc[0]['PubMed_ID']
    else:
        pubmed = '--'

    if(uni_id in list(UNI_PDB['UniProt_ID'])):
        pdb = UNI_PDB.loc[UNI_PDB['UniProt_ID'] == uni_id, ['PDB_ID']].iloc[0]['PDB_ID']
    else:
        pdb = '--'
        
    if (pdb != '--' or pubmed != '--'):
        master_df = master_df.append({'Uniprot_id' : uni_id, 'Pubmed_links':pubmed, 'PDB_ids':pdb},ignore_index=True)


print(master_df)

master_df.to_csv("Master_list.csv",index=False)
