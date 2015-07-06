import sys
import CADD_prescored as cp
import os
import numpy as np
import argparse
import re

def input_read():
  parser = argparse.ArgumentParser(description="""
  setup: Sets up the class object.
  query: this mode can be used to query the table for the scores.""")#TODO remove the setup setp if it is unlikely to have many datasets from the same setup.
  parser.add_argument('score_folder', metavar='<folder_containing_scores>', help='path to the folder containing scores *local path')
  parser.add_argument('-s', '--setup', action='store_true', help='Run once for the dataset to setup the class object for looking up')
  parser.add_argument('-q', '--query', metavar='<mutation_file.vcf>', nargs=1, help='-q or --query flag should be followed by the mutation data file <mute_file.vcf>', default=False)
  args = parser.parse_args()
  return args

def main():
  args = input_read()
  data_file = args.query[0]
  score_file = args.score_folder
  forward_backward_dic = {'.':'.', 'A':'T', 'C':'G', 'T':'A', 'G':'C'}

  PWD = os.path.dirname(os.path.realpath(__file__))

  if args.setup:
    tbx = cp.TabixID(PWD + '/'+ score_file + 'whole_genome_SNVs.tsv.gz', PWD + '/' + score_file + '/InDels.tsv.gz')
    tbx.setup_index()

  if args.query: # default is false
    tbx = cp.TabixID(PWD + '/' + score_file + 'whole_genome_SNVs.tsv.gz', PWD + '/' + score_file + '/InDels.tsv.gz')
    # Read in the mutation data
    datafp = open(PWD + '/' + data_file, 'r')
    data = datafp.read().splitlines()
    datafp.close()
    data = np.flipud(np.array([row.split(',')[0].split('\t') for row in data][1:])) # get rid of the first row
    # data is an array things similar to this: ['14' '23902893' '.' ..., '.' '.' '.']
    chr = data[1,0]
    start = data[0,1]
    end = data[np.shape(data)[0]-1,1]
    # Generate the relevant parts of the scores
    tbx.local_table(chr, start, end)
    # query the database
    scores = [tbx.query(item[1], forward_backward_dic.get(item[3], item[3]), forward_backward_dic.get(item[4], item[4])) for item in data ]
    # Find the file name
    file_name = re.search(r"/(\w+).vcf", data_file).groups()[0]
    # write the file.
    results_fp = open(PWD+'/../results/CADD_'+file_name+'.txt', 'w')
    results_fp.write(str(scores))
    results_fp.close()

if __name__=='__main__':
  main()

  

