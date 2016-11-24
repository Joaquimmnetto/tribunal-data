import datetime
import pickle
import sys
#from nltk.tokenize import TweetTokenizer

#vocab construido por build_vocab.sh
corpus_vocab_fl = "../../../data/vocabs/offender.vocab" if len(sys.argv) < 2 else sys.argv[1]
min_freq = 50

ct = 0
last_ct = 0
vocab_freq = dict()


with open(corpus_vocab_fl,'r',encoding='utf-8') as vocab:
	print("Building Vocabulary")
	for line in vocab:
		if ct - last_ct > 10000:
			print(datetime.datetime.now())
			last_ct = ct
		ct = ct + 1
		#tk_line = TweetTokenizer(reduce_len=True).tokenize(line.lower())
		tk_line = line.replace('\n', '').split(sep=" ")

		if tk_line[0].strip() == '':
			freq = int(tk_line[1])
			word = tk_line[2]
		else:
			freq = int(tk_line[0])
			word = tk_line[1]


		if freq >= min_freq:
			vocab_freq[word] = freq
		else:
			break

words = sorted(vocab_freq.keys())


print("Saving vocab_freq binary")
with open("bin/vocab_freq.pkl", 'wb') as output:
	pickle.dump(vocab_freq, output, pickle.HIGHEST_PROTOCOL)

print("Saving words binary")
with open("bin/words.pkl", 'wb') as output:
	pickle.dump(words, output, pickle.HIGHEST_PROTOCOL)

