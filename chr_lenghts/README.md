From raw fastas of the pangenome, obtain the index file running:
```
samtools faidx <genome.fasta>
```

Then, to obtain the file necessary for plotting:

```
python3 fai2lenghts.py <genome.fai>
```

Afterwards, you will need a unique file with all genomes that you want to plot:
```
cat <genome1_lenghts.txt> <genome2_lenghts.txt> ... <genomeN_lenghts.txt> > pangenome_ChrLenghts.txt
```
> Do not forget your reference genome
