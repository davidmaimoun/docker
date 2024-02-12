import os
import argparse

SEROGROUPING_DOCKER_APP_DIR = '/app/serogrouping'

def runCdcSerogroupPrediction(in_dir, out_dir):
    os.system(f'python3 {SEROGROUPING_DOCKER_APP_DIR}/characterize_neisseria_capsule.py -d {in_dir} -o {out_dir}')


parser = argparse.ArgumentParser(description="Get your samples serogroup (feat CDC)")
parser.add_argument("--input-dir", dest="input", required=True, help="Here your assemblies directory")
parser.add_argument("--output-dir", dest="output", required=True, help="Here your destination directory")

args = parser.parse_args()

runCdcSerogroupPrediction(args.input, args.output)
