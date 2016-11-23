import datetime
import pickle
import sys
from nltk.tokenize import TweetTokenizer

corpus_fl = "../../corpus_line.txt" if len(sys.argv) < 2 else sys.argv[1]

ct = 0
last_ct = 0
vocab_freq = dict()
first_words = set()

with open(corpus_fl,'r',encoding='utf-8') as corpus:
	print("Building Vocabulary")
	for line in corpus:
		if ct - last_ct > 500000:
			print(datetime.datetime.now())
			last_ct = ct
		ct = ct + 1
		tk_line = TweetTokenizer(reduce_len=True).tokenize(line.lower())

		first_words.add(tk_line[0]) if len(tk_line) > 0 else None

		for token in tk_line:
			if token not in vocab_freq.keys():
				vocab_freq[token] = 0
			vocab_freq[token] += 1

to_remove = []
for word,freq in vocab_freq.items():
	if freq < 50:
		to_remove.append(word)

for word in to_remove:
	del vocab_freq[word]
	try:
		first_words.remove(word)
	except:
		pass



print("Saving vocab_freq binary")
with open("vocab_freq.pkl", 'wb') as output:
	pickle.dump(vocab_freq, output, pickle.HIGHEST_PROTOCOL)
print("Saving first_words binary")
with open("first_words.pkl",'wb') as output:
	pickle.dump(first_words, output, pickle.HIGHEST_PROTOCOL)
