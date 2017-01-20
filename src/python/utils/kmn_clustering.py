#http://fraka6.blogspot.com.br/2013/04/kmeans-with-configurable-distance.html
#from sklearn.cluster import KMeans
import sklearn.metrics

from sklearn.cluster import KMeans
import datetime
import pickle
import numpy as np
from gensim.models.doc2vec import Doc2Vec

import args_proc as args

docs = pickle.load(open(args.d2v_team_r2d,'rb'))

def load_d2v(data_fn):
	d2v_model = Doc2Vec.load(data_fn)
	d2v_model.init_sims(replace=True)
	d2v_mat = np.array(d2v_model.docvecs)
	del d2v_model
	return d2v_mat


def kmn_clustering(data, num_clusters):
	#Todo: KMN usando cosseno ;=;
	kmn_model = KMeans(n_clusters=num_clusters, n_jobs=1)

	# gambiarra pra usar coseno no sklearn
	import sklearn.metrics.pairwise
	from sklearn.metrics.pairwise import cosine_distances
	def new_euclidean_distances(X, Y=None, Y_norm_squared=None, squared=False):
		return cosine_distances(X, Y)
	real_euclid_dist = sklearn.metrics.pairwise.euclidean_distances

	sklearn.metrics.pairwise.euclidean_distances = new_euclidean_distances


	kmn_model.fit(data)
	labels = kmn_model.predict(data)
	distances = kmn_model.transform(data)

	sklearn.metrics.pairwise.euclidean_distances = real_euclid_dist

	return labels,distances


d2v_mat = load_d2v(args.d2v_team)
before = datetime.datetime.now()
data = d2v_mat[0:100]
for n_cl in range(2,11):
	labels, distances = kmn_clustering(data, n_cl)
	silhouette = sklearn.metrics.silhouette_score(data, labels, metric='cosine') #varia de -1 a 1
	print("For",n_cl,"clusters")
	print("Silhouette: ",silhouette)



docs = [docs[i] for i in range(0,len(docs.keys()))]
res = list(zip(docs,labels))

#pprint(res)


print("Time elapsed:", datetime.datetime.now()-before)

