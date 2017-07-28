import math
from pprint import pprint

import scipy.io
import numpy as np
from matplotlib import pylab,pyplot

from gensim.models.doc2vec import Doc2Vec
from spherecluster import SphericalKMeans
from bhtsne import tsne

import sklearn
import pandas as pd

from ggplot import *
from sklearn.cluster import AgglomerativeClustering

from sil_metric import silhouette_score_block
#import args_proc as args
from params import args, clt, vecs, model_dir
import utils




def load_tfidf(data_fn):
  tfidf_mat = scipy.io.mmread(data_fn)
  return tfidf_mat


def load_d2v(data_fn):
  d2v_model = Doc2Vec.load(data_fn)
  d2v_model.init_sims(replace=True)
  d2v_mat = np.array(d2v_model.docvecs, dtype=np.float64)

  d2v_mat = sklearn.preprocessing.normalize(d2v_mat, norm='max', copy=False)

  del d2v_model
  return d2v_mat


def plot_2dmatrix(matrix, filename):

  pylab.cla()
  pylab.clf()
  pylab.bone()
  for i, pos in enumerate(matrix):
    pylab.plot(pos[0], pos[1], 'o', markerfacecolor='blue', markersize=3, markeredgewidth=2)
  pylab.savefig(filename)


def buckshot_smpl(data, num_cl):
  n_smpl = int(math.ceil(math.sqrt(num_cl * data.shape[0])))
  smpl_data = data[np.random.randint(data.shape[0], size=n_smpl), :]

  return smpl_data


# Mining text data cap.4 sec.3.3
def buckshot(smpl_data, num_cl):
  labels = AgglomerativeClustering(n_clusters=num_cl, linkage='complete', affinity='cosine').fit_predict(smpl_data)

  centers = np.zeros((num_cl,smpl_data.shape[1]))
  l, counts = np.unique(labels, return_counts=True)
  del l
  for label, data in zip(labels, smpl_data):
    centers[label] += data / counts[label]

  return np.array(centers)


def kmeans(data, centers, n_clusters):
  kmn_model = SphericalKMeans(n_clusters=n_clusters, init=centers)
  #kmn_model = SphericalKMeans(n_clusters=n_clusters)
  labels = kmn_model.fit_predict(data)
  kmn_centers = kmn_model.cluster_centers_
  return labels, kmn_centers


def do_clusterization(data, n_clusters):
  print("Applying aggl on subdata to imporove starting centers...")
  smpl = buckshot_smpl(data, n_clusters)
  centers = buckshot(smpl, n_clusters)

  print("Applying kmeans on the data")
  labels = kmeans(data, centers, n_clusters)

  return labels


def silhouette_analysis(data, smpl_size):
  if smpl_size > 0:
    sample = data[np.random.choice(data.shape[0], size=smpl_size, replace=False), :]
  else:
    sample = data

  silhouettes = []
  calinskis = []
  print("Testing silhouettes...")
  for n_cl in range(2, 20, 1):
    labels, centers = do_clusterization(sample, n_cl)
    print("Processing silhouette")
    sil = silhouette_score_block(sample, labels, metric='cosine', n_jobs=2)
    cal = sklearn.metrics.calinski_harabaz_score(sample, labels)
    print("Silhouette (", n_cl, ") = ", sil)
    print("Calinski (", n_cl, ") = ", cal)

    silhouettes.append((n_cl, sil))
    calinskis.append((n_cl, cal))
  return silhouettes, calinskis

def plot_results(points, labels):

  d2_points = tsne(points, dimensions=3,rand_seed= 1)

  import matplotlib.pyplot as plt
  from mpl_toolkits.mplot3d import Axes3D
  fig = plt.figure()
  ax = fig.add_subplot(111, projection='3d')
  ax.scatter(d2_points[:, 0], d2_points[:, 1], d2_points[:, 2], c=labels)

  #pyplot.scatter(d2_points[:, 0], d2_points[:, 1], c=labels)
  pyplot.show()
  pyplot.savefig("points.png")


def main():
  n_clusters = int(args.get('n_clusters', 8))
  sil_testing = bool(args.get('sil_testing', "False")=="True")
  sampling = bool(args.get('sampling', "True") == "True")
  smpl_size = int(args.get('smpl_size', 10000))

  print("Loading matrix...")
  data = load_d2v(vecs.d2v.mtx)

  if sil_testing:

    silhouettes, calinskis = silhouette_analysis(data, smpl_size)
    print("silhouettes:")
    pprint(silhouettes)

    print()
    print("calinskis:")
    pprint(calinskis)

    plot_2dmatrix(silhouettes, "smpl_silhouettes_" + model_dir.replace('/', '#') + ".jpg")
    plot_2dmatrix(calinskis, "smpl_calinskis_" + model_dir.replace('/', '#') + ".jpg")

  else:
    print("clustering...")
    if sampling:
      data = data[np.random.choice(data.shape[0], size=smpl_size, replace=False), :]
      labels, kmn_centers = do_clusterization(data, n_clusters)

      plot_results(data,labels)
    else:
      labels,kmn_centers = do_clusterization(data, n_clusters)

    print("Saving labels...")
    utils.save_pkl(clt.kmn.labels, labels.tolist())
    utils.save_pkl(clt.kmn.r2d, labels.tolist())


if __name__ == '__main__':
  utils.measure_time(main)
