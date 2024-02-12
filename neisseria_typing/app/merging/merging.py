import pandas as pd
import sys
import json


def determineSerogroup(in_dir):
    matchs = {}
    with open(in_dir) as json_file:
        data = json.load(json_file)

    samples = data.get('Serogroup', [])
    for sample in samples:
        if sample['sample_name'] is not None and sample['predicted_sg'] is not None:
            matchs[sample['sample_name']] = sample['predicted_sg']
    return matchs

typing_file = sys.argv[1]
serogrouping_results = sys.argv[2]
output_file = "typing_serogrouping_report.csv"

serogrouping_match = determineSerogroup(serogrouping_results)

columns = ['Sample', 'Serogroup']
serogrouping_df = pd.DataFrame(list(serogrouping_match.items()), columns=columns)
typing_df = pd.read_csv(typing_file, index_col=False) # Prevent the date field to be index

merged_df = typing_df.merge(serogrouping_df, on="Sample")
merged_df.to_csv('output_file', index=False)

