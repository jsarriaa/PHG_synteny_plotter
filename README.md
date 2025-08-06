## Introduction

Pangenomes are powerful tools for uncovering structural variation among varieties at a chromosomal level. However, their complexity makes them difficult to visualize, especially in plants, which tend to have large genomes with a high proportion of repetitive sequences.

This guide documents a workflow to visualize a haplotype-based pangenome generated using [PHGv2](https://github.com/maize-genetics/phg_v2), with the help of the [SyntenyPlotteR](https://github.com/Farre-lab/syntenyPlotteR) R package.

The database used in this example is not yet public, but the code provided can be adapted by any user with their own PHG database. It is generated from 12 barley genomes + its reference used for build the PGH database (MorexV3 in this case).

> **PHGv2 version used for the database:**
> ```
> phg --version
> phg version 2.4.66.221
> ```

### Environment Setup

To reproduce the plots, create the conda environment:
```bash
conda env create -f syntenyplotter_env.yml
```
Once inside the environment, ensure that the SyntenyPlotteR library is installed and loaded in R:
```R
install.packages("syntenyPlotteR")
library(syntenyPlotteR)
```



The starting point will be:
- [h.vcf files](https://phg.maizegenetics.net/build_and_load/#create-vcf-files) output of a PHG database. Find here the **[Example database](https://github.com/jsarriaa/PHG_synteny_plotter/tree/main/hvcf_files)**
- **Indexed genomes** with chromosomes lenghts. Find here the **[Example dataset](https://github.com/jsarriaa/PHG_synteny_plotter/tree/main/chr_lenghts)** and instructions about how to build them with [Samtools](https://github.com/samtools/samtools).

However, SyntenyPlotteR package works with *.txt* files. Use those scripts to transform the data:

### From ```h.vcf.gz``` files to ```alignment.txt```
There is an intermediate step, going through ```.bed``` files.
```python
python3 hvcf2bed.py <input.h.vcf.gz>
```
As output you will get: ```input.h_alignment.txt```

This file is actually already an alignment between the reference genome used to build the PHG database and your query genome providing from the ```h.vcf.gz``` file.

### From ```.fai``` to ```chr_lenghts.txt```
From ```.fai``` files, run:
```python
python3 fai2lenghts.py <genome.fai>
```

For  every plot you will need all chromosomes lenghts from all genomes involved, even for the reference genome. You can use ```cat``` in _linux_ to easy and quiclky arm the file.
```
cat <genome1_lenghts.txt> <genome2_lenghts.txt> ... <genomeN_lenghts.txt> > pangenome_ChrLenghts.txt
```

### Stacking alignments
All those alignments alignments are only againts the reference genome used to build the pangenome. This is suitable to plot structural variation of haplotype ranges from the reference to your query genome, but yt may be convinient to concatenate several alignments in order to plot the whole pangenome one genome against the following one, and not all only against the reference.

Current alignments are:
```
Alignment_1.txt                                                                                                Alignment_2.txt
                                 chr1                                 chr2
Reference        │───────────────────────────────────│    │───────────────────────────────────│   .......      Reference       │───────────────────────────────────│    │───────────────────────────────────│   ......
                    I  I  I  I  I  I  I  I  I  I  I          I  I  I  I  I  I  I  I  I  I  I                                       I  I  I  I  I  I  I  I  I  I  I          I  I  I  I  I  I  I  I  I  I  I
Genome 1         │───────────────────────────────────│    │───────────────────────────────────│   .......      Genome 2        │───────────────────────────────────│    │───────────────────────────────────│   .......
```
Which are suitable for simple plots, but it is needed to modify the alignments if we want to plot the pangenome as a whole, and have something similar to:
```                                                                                         
                                 chr1                                 chr2
Reference        │───────────────────────────────────│    │───────────────────────────────────│   .......
                  I  I  I  I  I  I  I  I  I  I  I  I        I  I  I  I  I  I  I  I  I  I  I  I
Genome 1         │───────────────────────────────────│    │───────────────────────────────────│   .......
                  I  I  I  I  I  I  I  I  I  I  I  I        I  I  I  I  I  I  I  I  I  I  I  I
Genome 2         │───────────────────────────────────│    │───────────────────────────────────│   .......
                  I  I  I  I  I  I  I  I  I  I  I  I        I  I  I  I  I  I  I  I  I  I  I  I
Genome 3         │───────────────────────────────────│    │───────────────────────────────────│   .......
```
Here, only the first genome is aligned against the reference; the following one is aligned against the last genome, and in this way you can concatenate as many as you desire.
This is not a natural outcome of PHG haplotype ranges, but you can always trace back through reference the hapltotype ranges.
Run this script giving all the comparations in the order that you want to plot.

```python
python3 synteny_plotter.py <haplo1_alignment_merged.txt> <haplo2_alignment_merged.txt> ... <haploN_alignment_merged.txt>
```
This will output a list of files, sorted by number: ```genome_pangenome_nº.txt```
> **NOTE** At this point you are manipulating the haplotype original blocks from PHG. Some information is lost or distorsionated along the process. This procedure is good to plot and visualize data for human-eye, nothing else. Do not progress with studies with those files.

### Merging haplotype ranges
alignment files will probably have several thousands of rows which SyntenyPlotteR will have to process. Most of the ranges are generated by PHG to distinguish among sequences, but physically are sticked to neighbour ranges. Merging them and treat them as a whole, will reduce the plot processing, final image size, and will make the plot less overload.
Run:
```python
python3 merge_haploblocks.py <input_file>
```

### Selecting inversions, translocations...
From here, test to only plot inversions, translocations...
- inversions: by filtring lines only with reverse ```-``` strand haplotypes.
> **NOTE**: This will plot all sequences that are inversed compaired to the Reference.
- Translocation: By filtring lines that have different reference and query genomes.
- Deletion/insertion: Filtring lines that have a increase/decrease of x % ammount of total bp at the haplotype block.

# Ploting with SyntenyPlotteR

