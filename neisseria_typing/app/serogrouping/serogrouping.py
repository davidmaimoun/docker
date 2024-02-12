
#!/usr/bin/env python3
import os
import glob
import csv
import sys

SEROGROUPING_DOCKER_APP_DIR = '/app/serogrouping'

def runCdcSerogroupPrediction(in_dir, out_dir):
    os.system(f'python3 {SEROGROUPING_DOCKER_APP_DIR}/characterize_neisseria_capsule.py -d {in_dir} -o {out_dir}')


if len(sys.argv) != 3:
    exit("""
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    You need 2 (and only 2) arguments: 
        1- The assemblies directory
        2- An output directory
    """)
assemblies = sys.argv[1]
output_dir = sys.argv[2]


runCdcSerogroupPrediction(assemblies, output_dir)
