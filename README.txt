#Auot_annotations

This repo contains some useful files for running ...


repo contains:
 -c_anot_to_VCF.py
 -data
 -ref_data
 -job.sh
 -scripts/
 --CADD_score.py
 --CADD_prescored.py
 --PROVEAN_lookup.py
 --provean.py
 -results/


c_anot_to_VCF.py: converts the data file in .csv to .vcf format ** NOTE: the input csv file needs to be ordered by the mutation location. **
data: folder contains the mutation data
ref_data: folder contains the exon positions from PDB chr37 data.
job.sh: shell file to generate the annotation files for ...
CADD_score.py: Stores the CADD scores in results
CADD_prescored.py: Helper functions
provean.py: Stores the PROVEAN scores in results
PROVEAN_lookup.py: Helper functions for provean.py

##dependencies: 
  annovar
  tabix
    job.sh requires annovar to be installed as a module. 
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
