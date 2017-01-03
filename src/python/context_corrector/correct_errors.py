import sys
import pickle

corpus_fn = "" if len(sys.argv) < 2 else sys.argv[1]
vocab_pkl = "" if len(sys.argv) < 3 else sys.argv[2]
err_fn = "" if len(sys.argv) < 4 else sys.argv[3]
out_fn = "" if len(sys.argv) < 5 else sys.argv[4]
vocab = pickle.load(vocab_pkl)

err = dict(zip(vocab.keys(),vocab.keys()))

del vocab

with open(err_fn,'r') as err_fl:
	for line in err_fl:
		values = line.split(',')
		right = values[0]
		wrongs = values[1]
		if wrongs.strip() != '':
			wrongs = wrongs.split('|')
			for wrong in wrongs:
				err[wrong] = right


with open(corpus_fn,'r') as corpus_fl:
     with open(out_fn,'w') as out_fl:
		for line in corpus_fl:
			for word in line.split(' '):
				out_fl.write(err[word])
				out_fl.write(" ")
			out_fl.write("\n")




