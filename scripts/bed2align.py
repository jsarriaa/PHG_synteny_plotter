import pandas as pd
import sys
import os

# If BED not provided, exit
if len(sys.argv) != 2:
    print("Usage: python3 bed2align.py <input.bed>")
    sys.exit(1)

# Get input BED file path
bed_file = sys.argv[1]

# Read the BED file
try:
    bed = pd.read_csv(bed_file, sep="\t", header=None)
except Exception as e:
    print(f"Error reading file: {e}")
    sys.exit(1)

# Check if at least 9 columns are present
if bed.shape[1] < 9:
    print("Error: input BED file does not have at least 9 columns.")
    sys.exit(1)

# Extract required columns:
# ref_chr, ref_start, ref_end, qry_chr, qry_start, qry_end, orientation, ref_name, qry_name
alignment = bed[[0, 1, 2, 6, 7, 8]].copy()
alignment["orientation"] = bed[3]
alignment["ref_name"] = "MorexV3"
alignment["qry_name"] = bed[5]

# Define output filename
output_file = os.path.splitext(os.path.basename(bed_file))[0] + "_alignment.txt"

# Save to output file
alignment.to_csv(output_file, sep="\t", index=False, header=False)

print(f"Alignment file saved as: {output_file}")
