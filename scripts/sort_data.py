import argparse
import re
import c_anot_to_VCF as cvcf
import csv
import operator

def input_read():
  parser = argparse.ArgumentParser(description='Sorts the .csv file by the mutation position')
  parser.add_argument('df_mut', metavar='<mut_data.csv>', help='.csv file containing the mutations to be sorted. Takes absolute paths', action = cvcf.CheckExt({'csv'}))
  parser.add_argument('df_out', metavar='<output_file.csv>', help='.csv file containing the sorted csv input file. Takes absolute path', action = cvcf.CheckExt({'csv'}))
  args = parser.parse_args()
  return args.df_mut, args.df_out

def pat_search(pat, txt):
  r = re.search(pat, txt)
  return int(r.group(0)) if r else 0

def main():

  # Open pointer
  inputs = input_read()
  df = inputs[0]
  outfile = inputs[1]

  mut_pos = []
  reader = csv.reader(open(df, 'rU'), dialect=csv.excel_tab, delimiter=',')
  data = list(reader)
  data.sort(key=lambda l:pat_search('[0-9]+', l[2]))
  with open (outfile, 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter = ',', dialect=csv.excel_tab)
    for row in data:
      writer.writerow(row)

if __name__=='__main__':
  main()
