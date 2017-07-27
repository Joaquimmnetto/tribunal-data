import math
from pprint import pprint

import scipy.io
import numpy as np
from matplotlib import pylab
from gensim.models.doc2vec import Doc2Vec
from spherecluster import SphericalKMeans

import sklearn
from sklearn.cluster import AgglomerativeClustering

from sil_metric import silhouette_score_block
#import args_proc as args
from params import args_, clt, vecs, model_dir
import utils




def load_tfidf(data_fn):
  tfidf_mat = scipy.io.mmread(data_fn)
  return tfidf_mat


def load_d2v(data_fn):
  d2v_model = Doc2Vec.load(data_fn)
  d2v_model.init_sims(replace=True)
  d2v_mat = np.array(d2v_model.docvecs)
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

  centers = [np.zeros(smpl_data.shape[1])] * num_cl
  l, counts = np.unique(labels, return_counts=True)
  del l
  for label, data in zip(labels, smpl_data):
    centers[label] += data / counts[label]

  return centers


def kmeans(data, centers, n_clusters):
  kmn_model = SphericalKMeans(n_clusters=n_clusters, init=centers)
  labels = kmn_model.fit_predict(data)
  return labels


def do_clusterization(data, n_clusters):
  print("Applying aggl on subdata to imporove starting centers...")
  smpl = buckshot_smpl(data, n_clusters)
  centers = buckshot(smpl, n_clusters)
  # centers = None
  print("Applying kmeans on the data")
  labels = kmeans(data, centers, n_clusters)

  return labels


def silhouette_analysis(data, smpl_size):
  if smpl_size > 0:
    sample = data[np.array(range(0, data.shape[0], int(data.shape[0] / smpl_size)))]
  else:
    sample = data
  print(sample.shape)
  silhouettes = []
  calinskis = []
  print("Testing silhouettes...")
  for n_cl in range(2, 51, 1):
    labels = do_clusterization(sample, n_cl)
    print("Processing silhouette")
    sil = silhouette_score_block(sample, labels, metric='cosine', n_jobs=2)
    cal = sklearn.metrics.calinski_harabaz_score(sample, labels)
    print("Silhouette (", n_cl, ") = ", sil)
    print("Calinski (", n_cl, ") = ", cal)

    silhouettes.append((n_cl, sil))
    calinskis.append((n_cl, cal))
  return silhouettes, calinskis


def main():
  n_clusters = int(args_.get('n_clusters', 10))
  sil_testing = bool(args_.get('sil_testing', False))
  
  print("Loading matrix...")
  data = load_d2v(vecs.d2v.mtx)
  print(data.shape)
  if sil_testing:
    smpl_size = 1000
    silhouettes, calinskis = silhouette_analysis(data, smpl_size)
    print("silhouettes:")
    pprint(silhouettes)

    print()
    print("calinskis:")
    pprint(calinskis)

    plot_2dmatrix(silhouettes, "smpl_silhouettes_" + model_dir.replace('/', '#') + ".jpg")
    plot_2dmatrix(calinskis, "smpl_calinskis_" + model_dir.replace('/', '#') + ".jpg")

  else:
    labels = do_clusterization(data, n_clusters)
    print("Saving labels...")
    utils.save_pkl(clt.kmn.labels, labels.tolist())


if __name__ == '__main__':
  utils.measure_time(main)
