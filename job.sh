#!/bin/bash

data_name="HCM_vars"
ref_file="MYH7"
PW="/srv/gsfs0/projects/bustamante/apoursh_projects/rot_1/VCF"
Protein="ENSP00000347507" # For MYH7

echo "Converting .csv to .vcf"

python $PW/c_anot_to_VCF.py $PW/data/$data_name.csv $PW/ref_data/$ref_file.txt

module add annovar
echo "Converting vcf to avinput"

convert2annovar.pl -format vcf4old $PW/data/$data_name.vcf>$PW/data/$data_name.avinput

echo "Bringing in humandb"


if [ ! -d "$PW/humandb" ]; then
  annotate_variation.pl -buildver hg19 -downdb -webfrom annovar refGene $TMP/humandb/
  annotate_variation.pl -buildver hg19 -downdb cytoBand $TMP/humandb/
  annotate_variation.pl -buildver hg19 -downdb genomicSuperDups $TMP/humandb/
  annotate_variation.pl -buildver hg19 -downdb -webfrom annovar esp6500siv2_all $TMP/humandb/
  annotate_variation.pl -buildver hg19 -downdb -webfrom annovar 1000g2014oct $TMP/humandb/
  annotate_variation.pl -buildver hg19 -downdb -webfrom annovar snp138 $TMP/humandb/
  annotate_variation.pl -buildver hg19 -downdb -webfrom annovar ljb26_all $TMP/humandb/
  annotate_variation.pl -buildver hg19 -downdb cadd $TMP/humandb
fi

# For sift score and Polyphen2 : http://annovar.openbioinformatics.org/en/latest/user-guide/filter/#-ljb23_all-annotation

table_annovar.pl $PW/data/$data_name.avinput $TMP/humandb/ -buildver hg19 -out $PW/results/$data_name\_table -remove -protocol refGene,cytoBand,ljb26_all -operation g,r,f -nastring . -csvout

# For PROVEAN

# check to see the dictionary file exists:

# Protein name should come from /srv/gsfs0/projects/bustamante/apoursh_projects/rot_1/VCF/Provean/Homo_sapiens.GRCh37.66.pep.all.fa
if [ ! -d "$PW/Provean/PROVEAN_scores_ensembl66_human.tsv.p"]; then
  python scripts/provean.py make_dic Provean/PROVEAN_scores_ensembl66_human.tsv
fi

python $PW/scripts/provean.py score $PW/Provean/PROVEAN_scores_ensembl66_human.tsv ENSP00000347507 $PW/data/HCM_vars.csv

#CADD score : http://annovar.openbioinformatics.org/en/latest/user-guide/filter/#cadd-annotations



#annotate_variation.pl -filter -dbtype ljb23_sift -buildver hg19 -out $PW/results/$data_name\_sift $PW/data/$data_name.avinput $TMP/humandb/


# run other stuff
