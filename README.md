## Introduction

Pangenomes are powerful tools for uncovering structural variation among varieties at the chromosomal level. However, their complexity makes them difficult to visualize—especially in plants, which tend to have large genomes with a high proportion of repetitive sequences.

This guide documents a workflow to visualize a haplotype-based pangenome generated using [PHGv2](https://github.com/maize-genetics/phg_v2), with the help of the [SyntenyPlotteR](https://github.com/Farre-lab/syntenyPlotteR) R package.

The database used in this example is not yet public, but the code provided can be adapted by any user with their own PHG database.

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

