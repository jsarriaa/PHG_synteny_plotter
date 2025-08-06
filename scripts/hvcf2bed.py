import sys
import gzip
import os
import re

def parse_vcf_lines(lines, genome_name):
    output_lines = []

    for line in lines:
        line = line.strip()
        
        # Match single-segment ALT line
        match1 = re.search(r'SampleName=([^,]+),Regions=([^:]+):(\d+)-(\d+),Checksum=([^,]+),RefChecksum=([^,]+),RefRange=([^:]+):(\d+)-(\d+)', line)
        if match1:
            genome, chr_, start, end, checksum, ref_checksum, ref_chr, ref_start, ref_end = match1.groups()
            strand = "+"
            start, end = int(start), int(end)
            if start > end:
                strand = "-"
                start, end = end, start

            output_lines.append(f"{chr_}\t{start}\t{end}\t{strand}\t{checksum}\t{genome}\t{ref_chr}\t{ref_start}\t{ref_end}\t{ref_checksum}")
            continue

        # Match multi-segment ALT line
        match2 = re.search(r'SampleName=([^,]+),Regions="([^"]+)",Checksum=([^,]+),RefChecksum=([^,]+),RefRange=([^:]+):(\d+)-(\d+)', line)
        if match2:
            genome, regions, checksum, ref_checksum, ref_chr, ref_start, ref_end = match2.groups()
            for segment in regions.split(","):
                m = re.match(r'([^:]+):(\d+)-(\d+)', segment)
                if m:
                    chr_, start, end = m.groups()
                    strand = "+"
                    start, end = int(start), int(end)
                    if start > end:
                        strand = "-"
                        start, end = end, start

                    output_lines.append(f"{chr_}\t{start}\t{end}\t{strand}\t{ref_checksum}\t{genome}\t{ref_chr}\t{ref_start}\t{ref_end}\t{checksum}")

    return output_lines

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 hvcf2bed.py <vcf_folder> <genome_name>")
        sys.exit(1)

    vcf_folder = sys.argv[1]
    genome_name = sys.argv[2]
    vcf_file = os.path.join(vcf_folder, f"{genome_name}.h.vcf.gz")
    bed_file = os.path.join(vcf_folder, f"{genome_name}.h.bed")

    if not os.path.exists(vcf_file):
        print(f"VCF file not found: {vcf_file}")
        sys.exit(1)

with gzip.open(vcf_file, "rt") as f:
    output = parse_vcf_lines(f, genome_name)

# Sort output lines by chromosome and start position
output_sorted = sorted(
    output,
    key=lambda x: (x.split("\t")[0], int(x.split("\t")[1]))
)

with open(bed_file, "w") as out:
    out.write("\n".join(output_sorted) + "\n")
