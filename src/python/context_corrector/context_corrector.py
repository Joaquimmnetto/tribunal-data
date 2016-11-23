from gensim.models import word2vec
import pickle
import csv
import math

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

model = word2vec.Word2Vec.load("bin/corpus_w2v.bin")

inserted_words = set()
vocab_freq_pair = sorted(vocab_freq.items(),key=lambda x:x[1],reverse=True)

sim_ratio = 0.5
synonms = dict()
errors = dict()
for word,freq in vocab_freq_pair:

	#if word not in inserted_words:
	similars = model.most_similar(word,topn=10)

	synonms[word] = [w for w,s in similars if s > 0.65]
	errors[word] = [w for w,s in similars if  s > 0.65 and similar(w,word,sim_ratio,vocab_freq)]

	syn_wr.writerow( [word]+['|'.join(synonms[word])] )
	err_wr.writerow( [word]+['|'.join(errors[word])] )


#inserted_words = inserted_words + errors








