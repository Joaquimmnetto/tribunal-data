import pickle
import numpy
import scipy.io
import sys


model_dir = "../../data/full/samples" if len(sys.argv) < 2 else sys.argv[1]

print("Loading neighbors matrix")
with open(model_dir+'/neigh.spy','rb') as neigh_input:
	neigh = scipy.io.mmread(neigh_input)
print("Loading vocabulary")
with open(model_dir+'/words.pkl','rb') as wr_input:
	words = pickle.load(wr_input)
print("Loading first words")
with open(model_dir+'/first_words.pkl','rb') as vocab_input:
	first_words = list(pickle.load(vocab_input))


print("Trimmed Vocab size:",len(words))
#print("Trimmed Neigh Vocab size:",len(neigh))


print("Applying markov model...")


for i in range(0,20):
	sentence_size = numpy.random.choice(range(3,7))
	initial = ""
	while len(initial) < 3:
		initial = numpy.random.choice(first_words)

	result = [initial]
	current = initial
	for j in range(1,sentence_size):
		current_index = words.index(current)
		prob_dist = neigh.getrow(current_index).toarray()[0] / numpy.sum(neigh.getrow(current_index).toarray()[0])
		current = numpy.random.choice(words,p=prob_dist)

		result.append(current)

	print(' '.join(result))

