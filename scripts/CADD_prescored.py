import subprocess
import csv
import StringIO
import os
import numpy as np
import sys


class TabixID(): #TODO make sure that the index file exists
  def __init__(self,snv_file_name, indel_file_name):
    self.snv_fname = snv_file_name
    self.indel_fname = indel_file_name
    self.snv_table = None
    self.indel_table = None
    self.snv_pointer = 0 # Corresponds to where to start looking from.
    self.indel_pointer = 0

  def setup_index(self):
    print "--Constructing indexing for CADD"
    arg_snv = "tabix -f -p vcf " + self.snv_fname
    arg_indel = "tabix -f -p vcf " + self.indel_fname
    #
    p1 = subprocess.Popen(arg_snv, shell=True)
    p2 = subprocess.Popen(arg_indel, shell=True)
    p1.communicate()
    p2.communicate()
    print "--CADD index construction has finished"

  def local_table(self,chr, start, end):
    # Command line to be executed in bash
    arg_snv = "tabix "+self.snv_fname+' '+chr+':'+start+'-'+end
    arg_indel = "tabix "+self.indel_fname+' '+chr+':'+start+'-'+end
    # Execute commands above
    snv_table = subprocess.check_output(arg_snv, shell=True)
    indel_table = subprocess.check_output(arg_indel, shell=True)
    # pointer to the string generated
    snv_tablefp = StringIO.StringIO(snv_table)
    indel_tablefp = StringIO.StringIO(indel_table)
    #
    self.snv_table = list(csv.reader(snv_tablefp, delimiter = '\t'))
    self.indel_table = list(csv.reader(indel_tablefp, delimiter = '\t'))
    self.snv_pos = [row[1] for row in self.snv_table]
    self.indel_pos = [row[1] for row in self.indel_table]

  def query(self,qposition, qref, qmut):
    # Del case:
    print qref, qmut, qposition
    if qmut == '.':
      try:
        first_indx = self.indel_pos[self.indel_pointer:].index(qposition)
        loc = first_indx + self.indel_pointer
        self.snv_pointer += first_indx
        i = 0
        while self.indel_table[loc + i] == qposition:
          if self.indel_table[loc + i][3] == qmut:
            score = (self.indel_table[loc + i][4], self.indel_table[loc + i][5])
            break
      except ValueError:
        score = ''
    # insert case
    elif qref == ".":
      sys.stderr.write("not implemented")
      pass #TODO
    # snv
    else:
      # Search in the local table from snv_pointer on to find the relevant position
      first_indx = self.snv_pos[self.snv_pointer:].index(qposition)
      loc = first_indx + self.snv_pointer
      self.snv_pointer += first_indx
      # Find which mutation in the group is in the data
      for i in range(3):
        if self.snv_table[loc + i][3] == qmut:
          score = (self.snv_table[loc + i][4], self.snv_table[loc + i][5])
    return score
    # fp = open(file_name, 'r')
    # print fp.read()
    # print "yo"
    # self.tb = tabix.Tabix(fp.read)


def main():
  PWD = os.path.dirname(os.path.realpath(__file__))
  scores = TabixID(PWD+'/../CADD_v1.2/prescored/whole_genome_SNVs.tsv.gz', PWD+'/../CADD_v1.2/prescored/InDels.tsv.gz')
  #scores.setup_index()
  print "here"
  #['14' '23902893' '.' ..., '.' '.' '.']


#   arg = "tabix -f -p vcf ../CADD_v1.2/prescored/whole_genome_SNVs.tsv.gz 14:23887458-23887607"
#   p=subprocess.check_output(arg,shell=True)
#   print 'this is p'
#   infile = StringIO.StringIO(p)
#   #r = csv.DictReader(infile, 
#   reader = csv.reader(infile, delimiter = '\t')
#   print reader# p.strip().split('\n').split('\n')
#   for line in reader:
#     print line[1]
# #  for chr, pos, a, b, score1, score2 in reader:
# #    print pos
#   return

if __name__=='__main__':
  main()

