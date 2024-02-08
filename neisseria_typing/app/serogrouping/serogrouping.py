
#!/usr/bin/env python3
import os
import glob
import csv
import sys

SEROGROUPING_DOCKER_APP_DIR = '/app/serogrouping'

def runCdcSerogroupPrediction(in_dir, out_dir):
    os.system(f'python3 {SEROGROUPING_DOCKER_APP_DIR}/characterize_neisseria_capsule.py -d {in_dir} -o {out_dir}')

def determineSerogroup(in_dir, out_dir):
    matchs = {}
    runCdcSerogroupPrediction(in_dir, out_dir)
    
    rs = glob.glob(os.path.join(out_dir, 'serogroup', '*.tab'))
    with open(rs[0], "r", encoding="utf8") as serogroups_file:
        tsv_reader = csv.DictReader(serogroups_file, delimiter="\t")
        for data in tsv_reader:
            sample = data["Query"]
            sg = data["SG"]
            matchs[sample] = sg

    return matchs 


if len(sys.argv) != 3:
    exit("""
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    You need 2 (and only 2) arguments: 
        1- The assemblies directory
        2- An output directory
    """)
assemblies = sys.argv[1]
output_dir = sys.argv[2]


serogroups_match = determineSerogroup(assemblies, output_dir)
    
serogrouping_report = f'serogrouping_report.csv'

with open(serogrouping_report, 'w') as f:
    f.write('Sample,Serogroup\n')
    for key in serogroups_match.keys():
        f.write(f'{key},{serogroups_match[key]}\n')

# os.system(f'rm -r {output_dir}')