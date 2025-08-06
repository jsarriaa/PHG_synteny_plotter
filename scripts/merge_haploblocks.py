# Script to merge and concatenate haplotype blocks from aligned synteny blocks

import argparse
import os
import sys
import pandas as pd 

# If not file provided, exit
if len(sys.argv) != 2:
    print("Usage: python3 merge_haploblocks.py <input_file>")
    sys.exit(1)

input_file = sys.argv[1]

# Read the input file
try:
    df = pd.read_csv(input_file, sep="\t", header=None)
except Exception as e:
    print(f"Error reading file: {e}")
    sys.exit(1)

# ref_chr, ref_start, ref_end, qry_chr, qry_start, qry_end, orientation, ref_name, qry_name
if df.shape[1] < 9:
    print("Error: input file does not have at least 9 columns.")
    sys.exit(1) 
df.columns = ["ref_chr", "ref_start", "ref_end", "qry_chr", "qry_start", "qry_end", "orientation", "ref_name", "qry_name"]

merged_rows = []
i = 0
while i < len(df):
    row = df.iloc[i].copy()
    # Try to merge consecutive rows with same orientation and chromosome
    while i + 1 < len(df):
        next_row = df.iloc[i + 1]
        if row["orientation"] == "+":
            can_merge = (
                row["qry_chr"] == next_row["qry_chr"] and
                row["orientation"] == next_row["orientation"] and
                row["qry_end"] + 1 == next_row["qry_start"]
            )
            if can_merge:
                # Extend end coordinates
                row["qry_end"] = next_row["qry_end"]
                row["ref_end"] = next_row["ref_end"]
                i += 1
            else:
                break
        elif row["orientation"] == "-":
            can_merge = (
                row["qry_chr"] == next_row["qry_chr"] and
                row["orientation"] == next_row["orientation"] and
                row["qry_start"] == next_row["qry_end"] + 1
            )
            if can_merge:
                # Extend start coordinates
                row["qry_start"] = next_row["qry_start"]
                row["ref_start"] = next_row["ref_start"]
                i += 1
            else:
                break
        else:
            break
    merged_rows.append(row)
    i += 1

# Output merged DataFrame
merged_df = pd.DataFrame(merged_rows)
output_file = os.path.splitext(input_file)[0] + "_merged.txt"
merged_df.to_csv(output_file, sep="\t", index=False, header=False)
print(f"Merged blocks written to {output_file}")
