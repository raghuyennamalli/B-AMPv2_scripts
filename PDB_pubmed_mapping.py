from requests_html import HTML, HTMLSession
import pandas as pd

base_url = "https://www.rcsb.org/structure/"
count = 0

df = pd.read_csv("PDB_ids.csv")
pdb_ids = list(df['PDB_ids'])

PMID = []

for index,pdb_id in enumerate(pdb_ids):
    res = HTMLSession().get(base_url+pdb_id)
    pmid = res.html.xpath("/html/body/div/div[3]/div[2]/div[1]/div/div[2]/div[4]/div/div/div[2]/div/ul/li[1]/a")
    if len(pmid) == 0:
        PMID.append("NaN")
    else:
        PMID.append(pmid[0].text)

    percent = int(((index+1)/3095) * 100)
    print ("="*percent + "> (" + str(percent) + "%) Mapped : " + str(index+1) + " ids\r",end='',flush=True)


pd.DataFrame({'PDB_ID':pdb_ids,'PMID':PMID}).to_csv("PDB_PubMed_mapping.csv",index=False)

