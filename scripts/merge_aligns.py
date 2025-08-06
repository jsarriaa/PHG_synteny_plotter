# Script to create a full pangenome synteny set of files, looking forward plot more than 1 genome + Morex
# Usage: python3 synteny_plotter.py <haplo1_alignment_merged.txt> <haplo2_alignment_merged.txt> ... <haploN_alignment_merged.txt>

import os
import sys
import subprocess   

verbose = True

if len(sys.argv) < 2:
    print("Usage: python3 synteny_plotter.py <haplo1_alignment_merged.txt> <haplo2_alignment_merged.txt> ... <haploN_alignment_merged.txt>")
    sys.exit(1)

# Get the list of alignment files from command line arguments
alignment_files = sys.argv[1:]

# Export names of alignment files. Create a hash to store the names
alignment_names = {}
for file in alignment_files:
    name = os.path.basename(file).split('.')[0]
    alignment_names[name] = file

print ("Alignment files to be processed:")
for name, file in alignment_names.items():
    print(f"{name}: {file}")

# Add the reference with no file
reference = "MorexV3"

# Sort the list. Always put the reference first
sorted_names = sorted(alignment_names.keys())

# set column names
column_names = ["ref_chr", "ref_start", "ref_end", "query_chr", "query_start", "query_end", "strand", "ref_name", "ref_name"]

# Iterate all over the alignment files.
# For the first one, keep the file as it is.
# Keep the name substituying ".txt" with "_pangenome.txt"

if verbose:
    print("#####################################")
    print("Creating pangenome synteny files...")
    print("#####################################")

last_processed_genome = None # initially no genome has been processed

for i, name in enumerate(sorted_names):

    # count number of genomes processed at this point
    if last_processed_genome is None:
        num_genomes = 1
    else:
        num_genomes = i + 1

    if verbose:
        print(f"Processing {name}...")

    file = alignment_names[name]
    output_file = f"{name}_pangenome_{num_genomes}.txt"

    if i == 0:
        # For the first file, we assume it is the reference
        with open(file, 'r') as infile, open(output_file, 'w') as outfile:
            # outfile.write("\t".join(column_names) + "\n") # do not print header
            for line in infile:
                outfile.write(line)
            last_processed_genome = name

    else:
        with open(alignment_names[name], 'r') as infile, open(output_file, 'w') as outfile, open(alignment_names[last_processed_genome], 'r') as previous_file:
            # For other files:
            # · Look for the line where reference (Morex) coordinates are equal in both files
            # · Write the line using as reference the query coordinates of the first file

            if verbose:
                print(f"Processing {name} with reference {last_processed_genome}...")

            # Read previous file into a dictionary keyed by (ref_start, ref_end)
            prev_coords = {}
            for line in previous_file:
                fields = line.strip().split('\t')
                # Use ref_start and ref_end from previous file (columns 1 and 2)
                ref_start, ref_end = fields[1], fields[2]
                prev_coords[(ref_start, ref_end)] = fields

            if verbose:
                print(f"Previous coordinates loaded for {last_processed_genome}.")
                print(f"see first 10 keys: {list(prev_coords.keys())[:10]}")

            for line in infile:
                fields = line.strip().split('\t')
                # Use ref_start and ref_end from current file (columns 1 and 2)
                ref_start, ref_end = fields[1], fields[2]                

                # Try to find a previous interval where ref_start is >= prev_start and < prev_end
                match_key = None
                for prev_start, prev_end in prev_coords.keys():
                    if prev_start <= ref_start < prev_end:
                        match_key = (prev_start, prev_end)
                        break
                if match_key:
                    prev_fields = prev_coords[match_key]
                    # Compose new line using described column_names order
                    new_line = [
                        fields[0],                # ref_chr from current
                        fields[1],                # ref_start from current
                        fields[2],                # ref_end from current
                        fields[3],                # query_chr from current
                        fields[4],                # query_start from current
                        fields[5],                # query_end from current
                        fields[6],                # strand from current
                        prev_fields[8],           # ref_name from previous
                        fields[8]                 # ref_name from current
                    ]
                    outfile.write("\t".join(new_line) + "\n")
            last_processed_genome = name
        
        # Check if the output file was created successfully and is not empty
        if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
            if verbose:
                print(f"Output file {output_file} created successfully.")
        else:
            print(f"Error: Output file {output_file} was not created or is empty.")
            sys.exit(1)
