import sys
import datetime
import pickle
import copy
import random
import numpy
import scipy.sparse
import scipy.io

import traceback



from nltk.tokenize import TweetTokenizer

corpus_fl = "../../../data/corpus/offender_tkn.crp" if len(sys.argv) < 2 else sys.argv[1]
# next_csv = "../../next_matrix.csv" if len(sys.argv) < 3 else sys.argv[2]

ct = 0
last_ct = 0

print("Carregando Vocabuário")
with open("bin/words.pkl",'rb') as wr_fl:
	words = pickle.load(wr_fl)


print("Alocando Matriz...")

w_indexes = dict((w,i) for i,w in enumerate(words))

vocab_len = len(words)
print("Vocab size:",vocab_len)
neigh = (numpy.zeros((vocab_len,vocab_len)))

first_words = set()

with open(corpus_fl,'r',encoding='utf-8') as corpus:
	print('Preenchendo Matriz...')
	for line in corpus:
		if ct - last_ct > 1000000:
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
				if i==0:
					first_words.add(token)
				neigh[w_index][n_index] += 1
			except:
				pass
				#traceback.print_exc()



print("Saving neigh")
with open("bin/neigh.spy",'wb') as output:
	#file object
	scipy.io.mmwrite(output, scipy.sparse.csr_matrix(neigh))

print("Saving first_words")
with open("bin/first_words.pkl",'wb') as output:
	#object file
	pickle.dump(first_words, output, pickle.HIGHEST_PROTOCOL)





