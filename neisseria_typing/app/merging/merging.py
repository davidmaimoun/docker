import pandas as pd
import sys

typing_file = sys.argv[1]
serogrouping_file = sys.argv[2]
output_file = "typing_serogrouping_report.csv"

serogrouping_df = pd.read_csv(serogrouping_file)
typing_df = pd.read_csv(typing_file, index_col=False) # Prevent the date field to be index

merged_df = typing_df.merge(serogrouping_df, on="Sample")
merged_df.to_csv(output_file, index=False)