import sys
from gensim.models import word2vec
from nltk.metrics.distance import edit_distance
import pickle
import datetime

models_dir = "../../data/full/samples" if len(sys.argv) < 2 else sys.argv[1]
max_edit_dist = 0.5 if len(sys.argv) < 3 else float(sys.argv[2])
min_sim = 0.60 if len(sys.argv) < 4 else float(sys.argv[3])
out_dir = models_dir if len(sys.argv) < 5 else sys.argv[4]

vocab_fn = models_dir + "/vocab_freq.pkl" if len(sys.argv) < 6 else models_dir + "/" + sys.argv[5]
w2v_fn = models_dir + "/w2v_model.bin" if len(sys.argv) < 7 else models_dir + "/" + sys.argv[6]
cor_fn = out_dir + "/corrector_dict.pkl" if len(sys.argv) < 8 else out_dir + "/" + sys.argv[7]
err_fn = out_dir + "/error_dict.pkl" if len(sys.argv) < 9 else out_dir + "/" + sys.argv[8]

#-----------------Metrics
#Generalized levenstein distance
def gld(s1,s2):
	return edit_distance(s1, s2)

#http://ieeexplore.ieee.org/document/4160958/
#Normalized Generalized levenstein distance
def ngld(s1,s2):
	alpha = 1
	dist = gld(s1,s2)
	ndist = 2 * dist / (alpha * (len(s1) + len(s2)) + dist)
	return ndist

def similar(s1,s2,max_edit_dist):
	dist = ngld(s1,s2)
	return dist < max_edit_dist


#-------------Logic
def load_w2v(w2v_filename):
	print("Loading word2vec file...")
	model = word2vec.Word2Vec.load(w2v_filename)
	model.init_sims(replace=False)
	return model


def _build_dicts(w2v_model, vocab_freq, sim_func, min_sim, max_edit_dist):

	vocab_freq_pair = sorted(vocab_freq.items(), key=lambda x: x[1], reverse=True)
	errors = dict()
	correction = dict()

	for word, freq in vocab_freq_pair:

		similars = w2v_model.most_similar(word, topn=50)
		errors[word] = [w for w, s in similars if s > min_sim and sim_func(w, word, max_edit_dist)]

		if len(errors[word]) > 0:
			tuples = list(zip(errors[word], [word] * len(errors[word])))
		else:
			tuples = [(word, word)]
		c = dict(tuples)
		correction.update(c)

	return errors,correction


def save_dicts(errors,correction,err_fn,cor_fn):
	print("Saving errors .pkl file")
	with open(err_fn, 'wb') as output:
		pickle.dump(errors, output, pickle.HIGHEST_PROTOCOL)

	print("Saving corrections .pkl file")
	with open(cor_fn, 'wb') as output:
		pickle.dump(correction, output, pickle.HIGHEST_PROTOCOL)


def build_dicts(max_edit_dist, min_sim, vocab_fn, w2v_fn, cor_fn, err_fn):
	with open(vocab_fn, "rb") as vocab_fl:
		vocab_freq = pickle.load(vocab_fl)

	print("Loading w2v model")
	w2v_model = load_w2v(w2v_fn)

	print("Looking for synonms and errors")
	errors, correction = _build_dicts(w2v_model, vocab_freq, similar, min_sim, max_edit_dist)

	save_dicts(errors, correction, err_fn, cor_fn)


begin_time = datetime.datetime.now()

build_dicts(max_edit_dist,min_sim,vocab_fn,w2v_fn,cor_fn,err_fn)

print("Time Elapsed:", datetime.datetime.now() - begin_time)




