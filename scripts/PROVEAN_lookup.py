#
#


import sys
import cPickle as pickle


class Provean_Score(object):
  def __init__(self, score_file):
    self.score_file = score_file

  def save_position(self):
    print "--Preparing position dictionary"
    seek_dic = {}
    fp = open(self.score_file, 'r')
    line = fp.readline() # this is the title
    pointer = fp.tell()
    line = fp.readline()  #first data line
    current_protein = line.split('\t')[0]
    num_aa = 1
    temp_pointer = fp.tell()
    line = fp.readline()
    while line != '':
      next_protein = line.split('\t')[0]
      if current_protein == next_protein:
        num_aa += 1
      else:
        seek_dic[str(current_protein)] = (pointer, num_aa)
        current_protein = next_protein
        pointer = temp_pointer
        num_aa = 1
      temp_pointer = fp.tell()
      line = fp.readline()

    fp.close()
    pickle.dump(seek_dic, open(self.score_file+'.p', 'wb'))

  def load_pos(self, pos, p_name):
    """pos = (position, length) as specified by save_position,
       p_name = nanme of the protein we are looking for"""
    print "--Extracting the relevant portion"
    p_provean = [None] * pos[1]
    with open(self.score_file) as fp:
      fp.seek(int(pos[0]))
      for i in range(pos[1]):
        p_provean[i] = fp.readline().split('\t')

    return p_provean



def main():
  file_name = '../Provean/PROVEAN_scores_ensembl66_human.tsv'
  scores = Provean_Score(file_name)
  scores.save_position()
  seek_dic=pickle.load(open(file_name+'.p', 'rb'))
  print scores.load_pos(seek_dic['ENSP00000387351'], 'ENSP00000387351')

  

if __name__=='__main__':
  main()





