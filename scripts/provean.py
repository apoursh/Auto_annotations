# runs Provean scores. In one setting (make_dic) it creates a dictionary that facilitates lookup.
# Creating the dictionary is a one time task for each score dataset.
#
# for comments or suggestions please contact a dot pourshafeie at gmail dot com

import sys
import cPickle as pickle
import PROVEAN_lookup as pv
from c_anot_to_VCF import CheckExt
import numpy as np
import re
import argparse


def input_read():
  parser = argparse.ArgumentParser(description="""
  make_dic: creates a dictionary of positions in the input file that correspond to the proteins. Take Provean database file in .txt format as input
  score computes the scores of the mutation in the input file. needs Provean score database, protein name, mutation file in csv format.""")
  parser.add_argument('score_file', metavar='<Provean_score.tsv>', help='The Provean score file to be used in tsv format. (absolute path)', action=CheckExt({'tsv'}))
  parser.add_argument('-d', '--make_dic', action='store_true', help='Constructs the indecies for faster lookup. This is only ncessary once for each provean score file.')
  parser.add_argument('-s', '--score', metavar='protein_name', help=" Protein name as specified in /srv/gsfs0/projects/bustamante/apoursh_projects/rot_1/VCF/Provean/Homo_sapiens.GRCh37.66.pep.all.fa")
  parser.add_argument('mut_file', metavar='<mutation_file.csv>', nargs='?',help='later', action=CheckExt({'csv'}), default='DeFaUlT.csv')

  args = parser.parse_args()
  return args

def amino_to_num(A):
  a_to_n_dic = {'':'','A':2, 'C':3, 'D':4, 'E':5, 'F':6, 'G':7, 'H':8, 'I':9, 'K':10, 'L':11, 'M':12, 'N':13, 'P':14, 'Q':15, 'R':16, 'S':17, 'T':18, 'V':19, 'W':20, 'Y':21, "Del":22}
  return [a_to_n_dic[item] for item in A]

def main():
  inputs = (input_read())
  if inputs.make_dic:
    PS = pv.Provean_Score(inputs.score_file)
    PS.save_position()

  if not inputs.make_dic and inputs.score is None:
    PS = pv.Provean_Score(inputs.score_file)
    protein_name =  inputs.score
    data_file = inputs.mut_file
    data_fp = open(data_file, 'r')
    data = data_fp.read().splitlines()
    data_fp.close()
    data = np.array([row.split(',') for row in data])
    seek_dic=pickle.load(open(inputs[0]+'.p', 'rb'))
    list = np.array(PS.load_pos(seek_dic[protein_name],protein_name))
    list[:,22] = [item[:-1] for item in list[:,22]]
    position = data[:,6]
    mut = amino_to_num(data[:,9])
    file_name = re.search(r"/(\w+).csv", data_file).groups()[0]
    results_fp = open('../results/provean_'+file_name+'.txt', 'w')
    results_fp.write(str([list[int(position[i])-1][mut[i]] for i in range(len(position))]))
    results_fp.close()


if __name__=='__main__':
  main()



