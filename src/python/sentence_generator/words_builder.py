import pickle
import numpy


with open('neigh.npy','rb') as neigh_input:
	neigh = numpy.load(neigh_input)

with open('vocab_freq.pkl','rb') as vocab_input:
	vocab_freq = pickle.load(vocab_input)

with open('first_words.pkl','rb') as vocab_input:
	first_words = list(pickle.load(vocab_input))


words = sorted(vocab_freq.keys())
print("Trimmed Vocab size:",len(words))
print("Trimmed Neigh Vocab size:",len(neigh))


print("Applying random model...")


for i in range(0,200):
	sentence_size = numpy.random.choice(range(3,7))
	initial = ""
	while len(initial) < 3:
		initial = numpy.random.choice(first_words)

	result = [initial]
	current = initial

	for i in range(1,sentence_size):
		current_index = words.index(current)
		prob_dist = neigh[current_index] / sum(neigh[current_index])
		current = numpy.random.choice(words,p=prob_dist)
		result.append(current)

	print(' '.join(result))

