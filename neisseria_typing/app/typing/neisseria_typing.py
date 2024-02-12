#!/usr/bin/env python3

import os
import sys
import json
from datetime import date, datetime
import argparse

NADA_PEPTIDE = 'NadA_peptide'
LOCI_MATCH=0
URL_NADA="https://rest.pubmlst.org/db/pubmlst_neisseria_seqdef/loci/NadA_peptide/sequence"
BEXERO = "Bexsero cross reactivity"
TRUMENBA = "Trumenba cross reactivity"

db_id  = {
    'mlst': "1", 'bast': "53", 'finetyping': "2",
    'B': '36', 'A': '29', 'C': '37', 'E': '35', 'H': '32', 'L': '33', 'W': '38',
    'X': '30', 'Y': '39', 'Z': '31'
}

alleles = {
    'bast':["PorA_VR1", "PorA_VR2", "NHBA_peptide", "fHbp_peptide", "NadA_peptide"],
    'mlst':['abcZ', 'adk', 'aroE', 'fumC', 'gdh', 'pdhC', 'pgm'] ,
    'finetyping': ['FetA_VR']
}
alleles_bast = ["PorA_VR1", "PorA_VR2", "NHBA_peptide", "fHbp_peptide", "NadA_peptide"]
alleles_mlst = ['abcZ', 'adk', 'aroE', 'fumC', 'gdh', 'pdhC', 'pgm']
keys_df = ['Date', 'Sample', 'ST', 'CC', 'BAST Type', 'PorA_VR1', 'PorA_VR2', 'NHBA_peptide', 'fHbp_peptide', 'NadA_peptide', \
    'abcZ', 'adk', 'aroE', 'fumC', 'gdh', 'pdhC', 'pgm', 'FetA_VR', 
    'Bexsero cross reactivity', 'Trumenba cross reactivity']
alleles_keys = ['PorA_VR1', 'PorA_VR2', 'NHBA_peptide', 'fHbp_peptide', 'NadA_peptide', \
    'abcZ', 'adk', 'aroE', 'fumC', 'gdh', 'pdhC', 'pgm', 'FetA_VR']


def fetchAlleleId(file, dict):
    if os.path.isfile(file):
        f = open(file)
        data = json.load(f)
        f.close()

        if 'exact_matches' in data:
            for i in data['exact_matches']:
                dict[i] = data['exact_matches'][i][0]['allele_id']
            return True
        else:
            return False
    else:
        return False

def fetchCCAndST(file): 
    f = open(file)
    data = json.load(f)
    f.close()
    if 'fields' in data:
        return data['fields']['clonal_complex'],  data['fields']['ST']
    else:
        return 'null', 'null'

def fetchBAST(bast_alleles, al, out_dir): 
    loci = populateURL(bast_alleles, al)

    cmd = f"""
        curl -s -H "Content-Type: application/json" \
        -X POST "https://rest.pubmlst.org/db/pubmlst_neisseria_seqdef/schemes/53/designations" \
        """
    cmd+= "-d '{\"designations\": { " + loci + " }}' > " + out_dir + "/bast_type.json"
   
    os.system(cmd)

    return getBastFromData(out_dir + "/bast_type.json")

def getBastFromData(file): 
    if os.path.isfile(file):
        f = open(file)
        data = json.load(f) 
        f.close()
        if 'fields' in data:
            return data['fields']
        else :
            return []
    else:
        return []

def getDbUrl(type):
    if type == 'nadA':
        return URL_NADA
    else:
        return f"https://rest.pubmlst.org/db/pubmlst_neisseria_seqdef/schemes/{db_id[type]}/sequence"

def getProfile(type, sequence, out_file):
   
    cmd="(echo -n '{\"base64\":true,\"sequence\": \"';base64 "
    cmd+=f"\"{sequence}\""
    cmd+="; echo '\"}') | "
    cmd+=f"""
        curl -s \
        -H "Content-Type: application/json" \
        -X POST {getDbUrl(type)} \
        -d @-  | jq . > {out_file} 
    """
   
    os.system(cmd)

# If it doesn't return a value to NadA_peptide, we want to look up for it
def getNadA(type, sequence, out_file):
    getProfile(type, sequence, out_file)

    if os.path.isfile(out_file):
        with open(out_file) as f:
            data = json.load(f)
            match = data['exact_matches']

        if len(match) > 0:
            alleles[NADA_PEPTIDE] = match[0]['allele_id']
    else:
        alleles[NADA_PEPTIDE] = "0"
    return 0
   
def populateURL(data, al):
    str = ''
    for val in data:
        if val in al:
            str += '"'+ val +'":[{"allele":"' + al[val] + '"}],'
    return str[:-1]


parser = argparse.ArgumentParser(description="Get your sample typing (MSLT, BAST, Finetyping, MenDeVar)")
parser.add_argument("--input", dest="assembly", required=True, help="Here your sample assembly")
parser.add_argument("--output", dest="output_dir", required=True, help="Here your destination directory")

args = parser.parse_args()

keys = "Date,Sample,ST,CC,BAST Type"
list_values = []

typing_data = {}
typing = {}
data = []

current_date = date.today().strftime("%d-%m-%Y")
current_time = datetime.now().strftime("%H:%M:%S")

sample = os.path.splitext(os.path.basename(args.assembly))[0]

for type in ['mlst', 'bast', 'finetyping']:
    out_file = os.path.join(args.output_dir, f"{sample}_{type}.json")

    getProfile(type, args.assembly, out_file)
    is_id = fetchAlleleId(out_file, typing)

    if is_id and type == 'mlst':
        cc, seq_type = fetchCCAndST(out_file)
if NADA_PEPTIDE not in typing:
    typing[NADA_PEPTIDE] = "0"

if typing[NADA_PEPTIDE] == "0":
    out_file = os.path.join(args.output_dir, f"{sample}_nada.json")
    getNadA('nadA', args.assembly, out_file)

data = fetchBAST(alleles_bast, typing, args.output_dir)
if len(data) == 0 :
    bast_type = 'null'
    bexsero = 'null'
    trumenba = 'null'
else:
    bast_type = data["BAST"]
    bexsero = data["MenDeVAR_Bexsero_reactivity"]
    trumenba = data["MenDeVAR_Trumenba_reactivity"]


values = f"{current_date},{sample},{seq_type},{cc},{bast_type},"
    

for key in alleles_keys:
    keys += f",{key}"
    if key in typing:
        values += f",{typing[key]}"
    else:
        values += f",null"
    

keys += ",Bexsero cross reactivity,Trumenba cross reactivity"
values += f",{bexsero},{trumenba}"


typing_report = f'{args.output_dir}/typing_report.csv'
if not os.path.exists(typing_report):
    with open(typing_report, 'w') as f:
        f.write(f'{keys}\n')
        f.write(f'{values}\n')
else:
    with open(typing_report,"a") as file:
        file.write(f'{values}\n')
