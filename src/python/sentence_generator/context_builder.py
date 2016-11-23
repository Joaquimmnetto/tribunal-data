import sys
import datetime
import pickle
import copy
import random
import numpy
import traceback


from nltk.tokenize import TweetTokenizer

corpus_fl = "corpus_trimmed.txt" if len(sys.argv) < 2 else sys.argv[1]
# next_csv = "../../next_matrix.csv" if len(sys.argv) < 3 else sys.argv[2]

ct = 0
last_ct = 0



with open("vocab_freq.pkl",'rb') as vf_fl:
	vocab_freq = pickle.load(vf_fl)


print("Alocando Matriz...")

words = sorted(vocab_freq.keys())
w_indexes = dict((w,i) for i,w in enumerate(words))
vocab_len = len(words)

inner_dict = dict( (w,0) for w in words)

neigh = numpy.zeros((vocab_len,vocab_len))

with open(corpus_fl,'r',encoding='utf-8') as corpus:
	print('Preenchendo Matriz...')
	for line in corpus:
		if ct - last_ct > 500000:
			print(datetime.datetime.now())
			last_ct = ct
		ct = ct+1

		# tk_line = TweetTokenizer(reduce_len=True).tokenize(line.lower())
		tk_line = line.replace('\n','').split(sep=" ")
		for i,token in enumerate(tk_line[:len(tk_line)-1]):
			next_w = tk_line[i + 1]
			try:
				w_index = w_indexes[token]
				n_index = w_indexes[next_w]
				neigh[w_index][n_index] += 1
			except:
				traceback.print_exc()





print("Saving neigh")
with open("neigh.npy",'wb') as output:
	numpy.save(output, neigh)





