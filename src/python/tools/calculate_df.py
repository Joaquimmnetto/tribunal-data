import numpy as np
import tools.utils as utils
from tools.params import base,vecs



def process_df(bow_mtx_fn):
  freq = None
  for i in range(0,vecs.n_matrix):
    print("Processing matrix",i)
    bow = utils.load_obj(bow_mtx_fn.format(i))
    if freq is None:
      freq = bow.sum(axis=0)
    else:
      freq  = freq + bow.sum(axis=0)

  freq = np.array(freq)[0]
  return freq


def main():
  df = process_df(vecs.bow.mtx)
  utils.save_pkl(vecs.df, df)

if __name__ == '__main__':
  utils.measure_time(main)