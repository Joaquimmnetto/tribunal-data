import pickle
import numpy

with open("dense_neigh.pkl",'rb') as neigh_fl:
	neigh = pickle.load(neigh_fl)
with open("vocab_freq.pkl",'rb') as vocab_fl:
	vocab_freq = pickle.load(vocab_fl)


words = sorted(vocab_freq.keys())

print("Trimmed Vocab size:",len(words))
print('Filling blanks...')
for extword in words:
	row_dict = neigh[extword]
	np_neigh = []
	for word in words:
		try:
			np_neigh.append(row_dict[word])
			pass
		except KeyError:
			np_neigh.append(0)

	neigh[extword] = numpy.array(np_neigh)


print("Saving sparse neigh")
with open("sparse_neigh.pkl",'wb') as output:
	pickle.dump(neigh, output, pickle.HIGHEST_PROTOCOL)

