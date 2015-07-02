# This script takes two files. A datafile containing the exon locations on a gene and an input file containing the mutations.

# Note, currently the data are taken from PDB which uses GRCH37 reference positions and the backward strand.

# Author: apoursh, Email: a.pourshafeie at gmail dot com

import sys
import re
import argparse
import os.path

def CheckExt(choices):
  class Act(argparse.Action):
    def __call__(self, parser, namespace, fname, option_string=None):
      ext = os.path.splitext(fname)[1][1:]
      if ext not in choices:
        option_string = '({})'.fomrat(option_string) if option_string else ''
        parser.error("file doesn't end with one of {}{}".format(choices, option_string))
      else:
        setattr(namespace, self.dest, fname)
  return Act

def input_read(): #Use argparse here.
  """reads in the data_file which contains the variants and the loc_file which contains the exon locations"""
  parser = argparse.ArgumentParser(description='converts a .csv file to .vcf format')
  parser.add_argument('df_mut', metavar='<mut_data.csv>', help='.csv file containing the mutations', action = CheckExt({'csv'}))
  parser.add_argument('df_loc', metavar='<exon_loc.txt>', help='.txt file containing the exon locations', action = CheckExt({'txt'}))
  args = parser.parse_args()
  return args.df_mut, args.df_loc

def cum_sum(A):
  tot = 0
  csum = [0 for i in A]
  for i in range(len(A)):
    tot += A[i]
    csum[i] = tot

  return csum

def position(Clength,starts, num):
  for row in range(1,len(Clength)):
    if Clength[row] - num > 0:
      return starts[row-1] + num-Clength[row-1]

def main():
  data_file_name, loc_file = input_read()
  # Read in the exon location file
  loc_file = open(loc_file, 'r')
  loc_data = loc_file.read()
  starts = []
  ends = []
  header = True
  chr = 0
  B = 0
  # Read the data file taken from PDB which contains the type, start, End locations
  for exon in loc_data.splitlines():
    if header:
      if not chr:
        chr = re.search('(?<=chr)\w+', exon).group(0)
      elif not B:
        B = int(re.search('(?<=Length coding sequence : )\d+', exon).group(0))
        header = False
    else:
      type, start, end = exon.strip().split("  ")
      start_noC = start.split(',')
      starts.append(int(''.join(start_noC)))
      end = end.split(',')
      ends.append(int(''.join(end)))
  starts.reverse()
  ends.reverse()
  length = [x1 - x2 + 1 for (x1, x2) in zip(ends, starts)] 
  cum_length = [0]+cum_sum(length)

  #Prepare the data_file
  mutated_seq = []
  pre_mutation = []
  post_mutation = []
  data_file = open(data_file_name, 'r')
  data = data_file.read()



  # Example: c.746G>Aa
  for mutation in data.splitlines():
    line = mutation.strip().split(",")
    gene,mutation_aa,mutation_seq,MaxLVT,classification,aa_wt3,aa_position,aa_mut3,aa_wt,aa_mut = mutation.strip().split(",")

    if mutation_seq != '':
      if aa_mut != 'Del':
        base_num = re.search('(?<=.)\w+',mutation_seq)
        #print base_num.group(0)[0:-1]
        mutated_seq.append(B-int(base_num.group(0)[0:-1])+3)
        post_mutation.append(mutation_seq[-1])
        pre_mutation.append(base_num.group(0)[-1])
      else:
        #base_num = re.search('(?<=.)\w+_\w+', mutation_seq)
        post_mutation.append(".")
        deleted = re.search('(?<=DEL)\w+', mutation_seq)
        pre_mutation.append(deleted.group(0))
        start_base = re.search('(\d+)_', mutation_seq)
        mutated_seq.append(B-int(start_base.group(1))+3)
  #print post_mutation
  data_w = open(data_file_name[:-3]+'vcf', 'w')
  header = ["#CHROM", "POS", "ID", "REF", "ALT", "QUAL", "FILTER", "INFO"]
  data_w.write('\t'.join(header))
  data_w.write('\n')

  for case in range(len(mutated_seq)):
    pos = position(cum_length,starts, mutated_seq[case])
    info = [chr, str(pos), '.', pre_mutation[case], post_mutation[case], ".", ".", "."]
    data_w.write('\t'.join(info))
    data_w.write('\n')



if __name__=='__main__':
  main()
