import csv

import numpy as np

import tools.utils as utils
from tools.params import vecs,clt,args


def export_labels(csv_fn, r2d_fn, r2l_fn, nparts):
  csv_wr = csv.writer(open(csv_fn, 'w',newline=""))
  r2d = utils.load(r2d_fn)          
  for part in range(0, nparts):
    r2l = utils.load(r2l_fn.format(part))
    for row,probs in r2l.items():      
      label = np.argmax(probs)
      csv_wr.writerow([*r2d[row], label])


def main():
  outp = args.get("output","results")
  export_labels("{0}.csv".format(outp),vecs.bow.r2d, clt.lda.r2l, vecs.n_matrix)

if __name__=='__main__':
  utils.measure_time(main) 