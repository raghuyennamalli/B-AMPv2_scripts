import requests
import pandas as pd
from collections import defaultdict

BASE = 'http://www.uniprot.org'
KB_ENDPOINT = '/uniprot/'
TOOL_ENDPOINT = '/uploadlists/'

df = pd.read_csv("D:\\academia\\YLab\\bamp_data\\scripts\\PDB_ids.txt",sep=",",header=None)
df = df.transpose()
df = df.rename({0: 'PDB_ids'}, axis='columns')

ids = df['PDB_ids'].to_list()

header = ['UniProt_ID', 'PDB_ID', 'Taxonomy_Lineage']
uni_id = dict()

for index, i in enumerate(ids[1700:2000]):
    params = {
        'from': 'PDB_ID',
        'to': 'ACC',
        'format': 'tab',
        'query': i
    }

    result = []
    pdb_req = requests.get(BASE+TOOL_ENDPOINT, params)
    uni_ids = pdb_req.text.split('\n')
    print (":::",index,uni_ids)
    del uni_ids[0]
    if uni_ids[-1] == '':
        del uni_ids[-1]
    for uid in uni_ids:
        result.append(uid.split('\t')[1])
    for uid in result:
        payload = {
            'query': f'id:"{uid}"',
            'format': 'tab',
            'columns': 'lineage(SUPERKINGDOM)'
        }

        meta_req = requests.get(BASE+KB_ENDPOINT, params=payload)
        metadata = meta_req.text.split('\n')[1].split('\t')
        if metadata[0] == 'Bacteria':
            uni_id[uid] = [i, metadata[0]]
    UniProt_PDB_mapping = pd.DataFrame([[key, uni_id[key][0], uni_id[key][1]] for key in uni_id.keys()], columns=header)
    UniProt_PDB_mapping.to_csv('UniProt_PDB_mapping_1700-2000.csv', index=False)
