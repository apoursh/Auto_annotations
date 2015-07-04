#Auot_annotations

This repo contains some useful files for running ...


repo contains:
 -c_anot_to_VCF.py
 -data
 -ref_data
 -job.sh


c_anot_to_VCF.py converts the data file in .csv to .vcf format
data folder contains the mutation data
ref_data folder contains the exon positions from PDB chr37 data.
job.sh shell file to generate the annotation files for ...


##dependencies: 
  annovar
    job.sh requires annovar to be installed as a module. 
  Provean scores
    The PROVEAN 1.1 scores can be found ftp://ftp.jcvi.org/pub/data/provean/precomputed_scores/
      mkdir Provean
      cd Provean/
      wget ftp://ftp.jcvi.org/pub/data/provean/precomputed_scores/*
      cd ../

