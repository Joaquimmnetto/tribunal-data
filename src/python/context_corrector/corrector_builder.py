import sys
from gensim.models import word2vec
from nltk.metrics.distance import edit_distance
import pickle
import csv
import datetime

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


begin_time = datetime.datetime.now()

vocab_fn = "../../../src/shell/out/chat_full_vocab_freq.pkl" if len(sys.argv) < 2 else sys.argv[1]
w2v_fn = "../../../src/shell/out/chat_full_tkn_w2v.bin" if len(sys.argv) < 3 else sys.argv[2]
max_edit_dist = 0.5 if len(sys.argv) < 4 else float(sys.argv[3])
min_sim = 0.60 if len(sys.argv) < 5 else float(sys.argv[4])
cor_fn = "bin/correct.pkl" if len(sys.argv) < 6 else sys.argv[5]
err_fn = "bin/errors.pkl" if len(sys.argv) < 7 else sys.argv[6]

#maneiras mais interessantes
#distancia de teclado
#coisa la que tem no slide de nlp

with open(vocab_fn,"rb") as vocab_fl:
	vocab_freq = pickle.load(vocab_fl)

#syn_fl = open(syn_fn,'w')
#syn_wr = csv.writer(syn_fl)
#err_fl = open(err_fn,'w')
#err_wr = csv.writer(err_fl)




print("Loading word2vec file...")
model = word2vec.Word2Vec.load(w2v_fn)
model.init_sims(replace=False)



vocab_freq_pair = sorted(vocab_freq.items(),key=lambda x:x[1],reverse=True)

print("Looking for synonms and errors")

#synonyms = dict()
errors = dict()
correction = dict()

for word,freq in vocab_freq_pair:

	similars = model.most_similar(word,topn=50)
	errors[word] = [w for w, s in similars if s > min_sim and similar(w, word, max_edit_dist)]
#	synonyms[word] = [w for w, s in similars if s > min_sim and w not in errors[word]]

	if len(errors[word]) > 0:
		tuples = list(zip(errors[word], [word] * len(errors[word])))
	else:
		tuples = [(word,word)]
	c = dict(tuples)
	correction.update(c)

#	syn_wr.writerow( [word] + ['|'.join(synonyms[word])] )
#	err_wr.writerow( [word]+['|'.join(errors[word])] )


#inserted_words = inserted_words + errors

print("Time Elapsed:",datetime.datetime.now()-begin_time)

print("Saving errors .pkl file")
with open(err_fn,'wb') as output:
	pickle.dump(errors,output,pickle.HIGHEST_PROTOCOL)

print("Saving corrections .pkl file")
with open(cor_fn, 'wb') as output:
	pickle.dump(correction, output, pickle.HIGHEST_PROTOCOL)




