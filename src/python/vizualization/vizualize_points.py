#import args_proc as args

import numpy as np
from ggplot import *
import pandas as pd

from sklearn.decomposition import PCA
from gensim.models import Doc2Vec
from bhtsne import tsne

from params import args,vecs
import utils


def load_bow_samples(sample_size):
  pass


def load_d2v_samples(sample_size):
  print("Loading model...")
  d2v_model = utils.load_obj(vecs.d2v.mtx, gensim_class=Doc2Vec)
  r2d = utils.load_obj(vecs.d2v.r2d)

  samples = np.random.choice(list(r2d.keys()), size=sample_size)

  return np.array([d2v_model.docvecs[int(index)] for index in samples],dtype=np.float64)


def tsne_reduction(points):
  print("Running Barnes-Hut TSNE")
  return tsne(points, dimensions=2)


def lda_reduction(points):
  pca = PCA(n_components=2)
  return pca.fit_transform(points)

def main():
  sample_size = args.get("sample_size", 100000)

  points = load_d2v_samples(sample_size)
  d2_points = tsne_reduction(points)

  print("Plotting results...")
  df_points = pd.DataFrame(d2_points,columns=["x","y"])
  plt = ggplot(df_points, aes(x="x",y="y")) + geom_point()

  plt.show()


if __name__ == '__main__':
  utils.measure_time(main)






