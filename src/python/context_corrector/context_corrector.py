import sys
from gensim.models import word2vec
import pickle
import csv
import math
import datetime

begin_time = datetime.datetime.now()

vocab_file = "bin/vocab_freq.pkl" if len(sys.argv) < 2 else sys.argv[1]
w2v_file = "bin/corpus_w2v.bin" if len(sys.argv) < 3 else sys.argv[2]
min_sim = 0.65 if len(sys.argv) < 4 else float(sys.argv[3])
min_word_sim = 0.50 if len(sys.argv) < 5 else float(sys.argv[4])

#maneiras mais interessantes
#distancia de teclado
#coisa la que tem no slide de nlp

with open("bin/vocab_freq.pkl","rb") as vocab_fl:
	vocab_freq = pickle.load(vocab_fl)

syn_fl = open("synonms.csv",'w')
syn_wr = csv.writer(syn_fl)
err_fl = open("errors.csv",'w')
err_wr = csv.writer(err_fl)

def similar(s1,s2,sim_ratio,vocab_freq):
	smaller = s1 if s1<s2 else s2
	bigger = s2 if smaller ==s1 else s1

	intersect = [c for c in smaller if c in bigger]

	#right = smaller if vocab_freq[smaller] > vocab_freq[bigger] else bigger

	return len(intersect) >= math.floor(sim_ratio * len(bigger))


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
	errors[word] = [w for w, s in similars if s > min_sim and similar(w, word, min_word_sim, vocab_freq)]
	synonyms[word] = [w for w, s in similars if s > min_sim and w not in errors[word]]


	syn_wr.writerow( [word] + ['|'.join(synonyms[word])] )
	err_wr.writerow( [word]+['|'.join(errors[word])] )


#inserted_words = inserted_words + errors

print("Time Elapsed:",begin_time-datetime.datetime.now())






