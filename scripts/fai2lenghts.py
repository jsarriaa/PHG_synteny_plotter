import sys
import os
import pandas as pd

if len(sys.argv) != 2:
    print("Usage: python3 fai_to_lengths.py <input.fai>")
    sys.exit(1)

fai_file = sys.argv[1]
basename = os.path.splitext(os.path.basename(fai_file))[0].replace(".fa", "")

# Read only the first two columns (chromosome, length)
df = pd.read_csv(fai_file, sep="\t", header=None, usecols=[0,1], names=["chr", "length"])

# Add the third column with the basename
df["genome"] = basename

# Save to file with suffix _lengths.txt
output_file = f"{basename}_lengths.txt"
df.to_csv(output_file, sep="\t", header=False, index=False)

print(f"Saved lengths with origin to {output_file}")
