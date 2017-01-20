
import datetime
import scipy.io
import numpy as np
from matplotlib import pylab
from gensim.models.doc2vec import Doc2Vec


from sklearn.decomposition import TruncatedSVD
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import mean_squared_error
from math import sqrt

import args_proc as args

def load_tfidf(data_fn):
	tfidf_mat = scipy.io.mmread(data_fn)
	return tfidf_mat

def load_d2v(data_fn):
	d2v_model = Doc2Vec.load(data_fn)
	d2v_model.init_sims(replace=True)
	d2v_mat = np.array(d2v_model.docvecs)

	del d2v_model

	return d2v_mat



def lsa_reduction(matrix,dim):
	lsa = TruncatedSVD(n_components = dim)
	return lsa.fit_transform(matrix)


def plot_2dmatrix(matrix,filename):
	pylab.cla()
	pylab.clf()
	pylab.bone()

	for i,pos in enumerate(matrix):
		#color = label_color(labels[i])
		pylab.plot(pos[0],pos[1],'o',markerfacecolor='None',markersize=5,markeredgewidth=2)

	#pylab.axis(axis)
	pylab.savefig(filename)


def aglCluster(data, num_cl, nn=None):
	if nn is not None:
		print("building nn")
		nn_model = NearestNeighbors(n_neighbors = nn, metric = 'cosine', algorithm = 'brute', n_jobs = 3)
		data_knn = nn_model.fit(data).kneighbors_graph(X = data, n_neighbors = nn, mode = 'distance')

		labels = AgglomerativeClustering(n_clusters=num_cl, linkage='complete', affinity='cosine',connectivity=data_knn).fit_predict(
			data)
	else:
		labels = AgglomerativeClustering(n_clusters=num_cl, linkage='complete', affinity='cosine').fit_predict(data)

	return labels


before = datetime.datetime.now()
print("Loading matrix...")

d2v_mat = load_d2v(args.d2v_team)

rms_res = dict()
d2v_actual_lb = aglCluster(d2v_mat[:10000], num_cl=10)


for nn in range(100,1001,100):
	print("\nnn =",nn)
	d2v_knn_lb = aglCluster(d2v_mat[:10000], num_cl=10, nn=nn)
	rms = sqrt(mean_squared_error(d2v_actual_lb, d2v_knn_lb))
	print("rms =",rms)
	rms_res[nn] = rms

from pprint import pprint
pprint(sorted(rms_res, key=rms_res.get, reverse=True))

#plot_2dmatrix(lsa2d,'tfidf_plot.jpg')
print("Time elapsed:", datetime.datetime.now()-before)

