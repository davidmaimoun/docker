import pandas as pd
import sys
import json
import argparse



def determineSerogroup(in_dir):
    matchs = {}
    with open(in_dir) as json_file:
        data = json.load(json_file)

    samples = data.get('Serogroup', [])
    for sample in samples:
        if sample['sample_name'] is not None and sample['predicted_sg'] is not None:
            matchs[sample['sample_name']] = sample['predicted_sg']
    return matchs

parser = argparse.ArgumentParser(description="Merging typing report and serogrouping result")
parser.add_argument("--typing", dest="typing_file", required=True, help="Here your typing CSV file")
parser.add_argument("--sg-dir", dest="serogrouping_results", required=True, help="Here your serogroup results directory (the serogrouping.py output)")
parser.add_argument("--output", dest="output", required=True, help="Here your destination directory")

args = parser.parse_args()

serogrouping_match = determineSerogroup(args.serogrouping_results)

columns = ['Sample', 'Serogroup']
serogrouping_df = pd.DataFrame(list(serogrouping_match.items()), columns=columns)
typing_df = pd.read_csv(args.typing_file, index_col=False) # Prevent the date field to be index

merged_df = typing_df.merge(serogrouping_df, on="Sample")
merged_df.to_csv(f"{args.output}/typing_final_report.csv", index=False)
