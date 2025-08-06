# Script to plot synteny. Modify the R script to suit your needs.

# Ensure you are working on the syntenyplotter_env
# conda activate syntenyplotter_env

print("Loading required libraries...")
library(syntenyPlotteR)

print("Plotting synteny...")
draw.linear(
  "Med11_full_concatenated_inversions",                                 # Set here your merged blocks file      
  "lenghts/Med11+GDB136_chrs_lenght.txt",                  # Set here your chromosome lengths file
"aligns/GDB_136_pangenome_1_merged_inversions.txt",
"aligns/HOR_10892_pangenome_2_merged_inversions.txt",
"aligns/HOR_1168_pangenome_3_merged_inversions.txt",
"aligns/HOR_12184_pangenome_4_merged_inversions.txt",
"aligns/HOR_13942_pangenome_5_merged_inversions.txt",
"aligns/HOR_14121_pangenome_6_merged_inversions.txt",
"aligns/HOR_21595_pangenome_7_merged_inversions.txt",
"aligns/HOR_21599_pangenome_8_merged_inversions.txt",
"aligns/HOR_2779_pangenome_9_merged_inversions.txt",
"aligns/HOR_2830_pangenome_10_merged_inversions.txt",
"aligns/HOR_3365_pangenome_11_merged_inversions.txt",
"aligns/HOR_3474_pangenome_12_merged_inversions.txt",
  fileformat = "pdf",
  colours = c(
    "chr1H" = "red",
    "chr2H" = "blue",
    "chr3H" = "green",
    "chr4H" = "orange",
    "chr5"  = "purple",
    "chr6H" = "yellow",  
    "chr7H" = "grey"
  ),
  w = 15,
  h = 12
)

# Move resulting PDFs from the temp directory to current working directory
tmp_dir <- tempdir()
pdf_files <- list.files(tmp_dir, pattern = "\\.pdf$", full.names = TRUE)

if (length(pdf_files) > 0) {
  file.copy(pdf_files, getwd(), overwrite = TRUE)
  message("Moved PDF files from temp to current directory:")
  print(basename(pdf_files))
} else {
  message("No PDF files found in temporary directory.")
}
