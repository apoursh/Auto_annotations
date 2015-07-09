#Auot_annotations

This repo contains some useful files for running ...


repo contains:
 -data
 -ref_data
 -job.sh
 -scripts/
 --sort_data.py
 --c_anot_to_VCF.py
 --CADD_score.py
 --CADD_prescored.py
 --PROVEAN_lookup.py
 --provean.py
 -results/




sort_data.py: Takes a scv file (filename.csv) and returns a csv file (sorted_filename.csv) sorted by the position of the mutation on DNA.
c_anot_to_VCF.py: converts the data file in .csv to .vcf format
data: folder contains the mutation data
ref_data: folder contains the exon positions from PDB chr37 data.
job.sh: shell file to generate the annotation files for ...
CADD_score.py: Stores the CADD scores in results
CADD_prescored.py: Helper functions
provean.py: Stores the PROVEAN scores in results
PROVEAN_lookup.py: Helper functions for provean.py

data:
The data should be in csv format with no headers. The expected columns are:
gene  mutation_aa mutation_seq  MaxLVT  classification  aa_wt3  aa_position aa_mut3 aa_wt aa_mut

ref_data:
The reference data can be copied from http://www.rcsb.org/pdb/gene/. The *Orientation* line, *UTR* linesi, title lines and *region length* and *phase at end* should then be deleted.
The beginning of the ref file for MYH7 is as follows:

Chromosome: chr14
Length coding sequence : 5805 nucleotides.
Exon  23,902,741  23,902,941
Exon  23,902,293  23,902,436
Exon  23,901,848  23,902,004

##dependencies:
  annovar
  tabix
    job.sh requires annovar/tabix to be installed as a module. If this is not the case, change job.sh as appropariate. i.e. install tabix/annovar as executibles and delete the relevant module laoding files. If annovar is installed, the humandb file may exist in the installation folder and can be used instead.
  Provean scores
    The PROVEAN 1.1 scores can be found ftp://ftp.jcvi.org/pub/data/provean/precomputed_scores/
      mkdir Provean
      cd Provean/
      wget ftp://ftp.jcvi.org/pub/data/provean/precomputed_scores/*
      cd ../
  CADD scores
    The CADD scores can be downloaded from http://cadd.gs.washington.edu/download.
      mkdir CADD_v1.2
      cd CADD_v1.2/
      wget http://krishna.gs.washington.edu/download/CADD/v1.2/whole_genome_SNVs.tsv.gz
      wget http://krishna.gs.washington.edu/download/CADD/v1.2/InDels.tsv.gz
      cd ../



