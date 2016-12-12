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

#tmp/token.tmp out/${1}_words.pkl out/${1}_neigh.spy out/${1}_fw.pkl
corpus_fl = "../../../data/corpus/offender_tkn.crp" if len(sys.argv) < 2 else sys.argv[1]
words_fl = "bin/words.pkl" if len(sys.argv) < 3 else sys.argv[2]
neigh_fl = "bin/neigh.spy" if len(sys.argv) < 4 else sys.argv[3]
fwords_fl = "bin/first_words.pkl" if len(sys.argv) < 5 else sys.argv[4]

# next_csv = "../../next_matrix.csv" if len(sys.argv) < 3 else sys.argv[2]


def create_neigh(words,corpus):
	ct = 0
	last_ct = 0

	vocab_len = len(words)
	print("Vocab size:", vocab_len)

	print("Alocando Matriz...")
	#neigh = (numpy.zeros((vocab_len, vocab_len)))
	neigh = scipy.sparse.coo_matrix((vocab_len, vocab_len)).todok()

	first_words = set()
	w_indexes = dict((w, i) for i, w in enumerate(words))


	print('Preenchendo Matriz...')

	for line in corpus:
		if ct - last_ct > 1000000:
			print(datetime.datetime.now())
			last_ct = ct
		ct = ct + 1

		# tk_line = TweetTokenizer(reduce_len=True).tokenize(line.lower())
		tk_line = line.replace('\n', '').split(sep=" ")
		#print(tk_line)
		for i, token in enumerate(tk_line[:len(tk_line) - 1]):
			next_w = tk_line[i + 1]
			try:
				w_index = w_indexes[token]
				n_index = w_indexes[next_w]

				if i == 0:
					first_words.add(token)
				neigh[w_index,n_index] += 1
			except:
				#print("Word not found (",token,")")
				pass
			# traceback.print_exc()
	return neigh,first_words
#-----------------------------------------------------------------
print("Carregando Vocabuário from ",words_fl)
with open(words_fl,'rb') as wr_fl:
	_words = pickle.load(wr_fl)

with open(corpus_fl,'r',encoding='utf-8') as _corpus:
	neigh,first_words = create_neigh(_words,_corpus)


print("Saving neigh on ",neigh_fl)
with open(neigh_fl,'wb') as output:
	#file object
	scipy.io.mmwrite(output, neigh.tocsr())

print("Saving first_words on ",fwords_fl)
with open(fwords_fl,'wb') as output:
	#object file
	pickle.dump(first_words, output, pickle.HIGHEST_PROTOCOL)



