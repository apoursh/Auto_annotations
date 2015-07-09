#!/bin/bash

data_name="TNNI3"
ref_file="TNNI3_test"
PW="/srv/gsfs0/projects/bustamante/apoursh_projects/rot_1/VCF"
Protein="ENSP00000341838" #"ENSP00000442795" #"ENSP00000347507" # For MYH7a


printf "\n%sSorting the data\n\n" '-'

python $PW/scripts/sort_data.py $PW/data/$data_name.csv $PW/data/sorted_$data_name.csv

printf "%sGenerating Sift and Polyphen2\n\n" '-'
echo "--Converting .csv to .vcf"

python $PW/scripts/c_anot_to_VCF.py $PW/data/sorted_$data_name.csv $PW/ref_data/$ref_file.txt

module load annovar
echo
echo "--Converting vcf to avinput"

convert2annovar.pl -format vcf4old $PW/data/sorted_$data_name.vcf>$PW/data/sorted_$data_name.avinput

echo
echo "--Bringing in humandb"


if [ ! -d "$PW/humandb" ]; then
  annotate_variation.pl -buildver hg19 -downdb -webfrom annovar refGene $PW/humandb/
  annotate_variation.pl -buildver hg19 -downdb cytoBand $PW/humandb/
  annotate_variation.pl -buildver hg19 -downdb genomicSuperDups $PW/humandb/
  annotate_variation.pl -buildver hg19 -downdb -webfrom annovar esp6500siv2_all $PW/humandb/
  annotate_variation.pl -buildver hg19 -downdb -webfrom annovar 1000g2014oct $PW/humandb/
  annotate_variation.pl -buildver hg19 -downdb -webfrom annovar snp138 $PW/humandb/
  annotate_variation.pl -buildver hg19 -downdb -webfrom annovar ljb26_all $PW/humandb/
  annotate_variation.pl -buildver hg19 -downdb cadd $PW/humandb
fi

# For sift score and Polyphen2 : http://annovar.openbioinformatics.org/en/latest/user-guide/filter/#-ljb23_all-annotation

table_annovar.pl $PW/data/sorted_$data_name.avinput $PW/humandb/ -buildver hg19 -out $PW/results/sorted_$data_name\_table -remove -protocol refGene,cytoBand,ljb26_all -operation g,r,f -nastring . -csvout



# For PROVEAN
echo
echo "-Generating Provean scores"
echo
# check to see the dictionary file exists:

# Protein name should come from /srv/gsfs0/projects/bustamante/apoursh_projects/rot_1/VCF/Provean/Homo_sapiens.GRCh37.66.pep.all.fa
if [ ! -e "$PW/Provean/PROVEAN_scores_ensembl66_human.tsv.p" ]; then
  echo
  echo "--Make Provean dictionary"
  python scripts/provean.py --make_dic Provean/PROVEAN_scores_ensembl66_human.tsv
fi

python $PW/scripts/provean.py --score $Protein $PW/Provean/PROVEAN_scores_ensembl66_human.tsv $PW/data/sorted_$data_name.csv

#CADD score : http://annovar.openbioinformatics.org/en/latest/user-guide/filter/#cadd-annotations

echo
echo "-Generating CADD scores"
echo

module load tabix

if [ ! -e "$PW/CADD_v1.2/whole_genome_SNVs.tsv.gz.tbi" ]; then
  echo
  echo "--tabix indexing"
  python scripts/CADD_score.py ../CADD_v1.2/ -s
fi

echo
echo "--generating scores"
python scripts/CADD_score.py ../CADD_v1.2/ -q ../data/sorted_$data_name.vcf


echo
echo "-PANTHER"
echo

#annotate_variation.pl -filter -dbtype ljb23_sift -buildver hg19 -out $PW/results/$data_name\_sift $PW/data/$data_name.avinput $TMP/humandb/


# run other stuff
