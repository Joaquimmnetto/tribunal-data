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
	ndist = 2 * dist / alpha * (len(s1) + len(s2)) + dist
	return ndist


def similar(s1,s2,max_edit_dist):
	dist = ngld(s1,s2)
	return dist < max_edit_dist


begin_time = datetime.datetime.now()

vocab_fn = "bin/vocab_freq.pkl" if len(sys.argv) < 2 else sys.argv[1]
w2v_file = "bin/corpus_w2v.bin" if len(sys.argv) < 3 else sys.argv[2]
max_edit_dist = 0.5 if len(sys.argv) < 4 else float(sys.argv[3])
syn_fn = "out/synonms.csv" if len(sys.argv) < 5 else sys.argv[4]
err_fn = "out/errors.csv" if len(sys.argv) < 6 else sys.argv[5]

#maneiras mais interessantes
#distancia de teclado
#coisa la que tem no slide de nlp

with open(vocab_fn,"rb") as vocab_fl:
	vocab_freq = pickle.load(vocab_fl)

syn_fl = open(syn_fn,'w')
syn_wr = csv.writer(syn_fl)
err_fl = open(err_fn,'w')
err_wr = csv.writer(err_fl)




print("Loading word2vec file...")
model = word2vec.Word2Vec.load("bin/offender_w2v.bin")
model.init_sims(replace=False)


inserted_words = set()
vocab_freq_pair = sorted(vocab_freq.items(),key=lambda x:x[1],reverse=True)

print("Looking for synonms and errors")

synonyms = dict()
errors = dict()

syn_wr.writerow(['word','synonyms'])
syn_wr.writerow(['word','possible_errors'])

for word,freq in vocab_freq_pair:
	if word in inserted_words:
		continue
	#if word not in inserted_words:
	similars = model.most_similar(word,topn=50)
	errors[word] = [w for w, s in similars if s > max_edit_dist and similar(w, word, max_edit_dist)]
	synonyms[word] = [w for w, s in similars if s > max_edit_dist and w not in errors[word]]


	syn_wr.writerow( [word] + ['|'.join(synonyms[word])] )
	err_wr.writerow( [word]+['|'.join(errors[word])] )


#inserted_words = inserted_words + errors

print("Time Elapsed:",begin_time-datetime.datetime.now())






