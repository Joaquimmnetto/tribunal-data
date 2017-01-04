import datetime
import pickle
import sys
#from nltk.tokenize import TweetTokenizer

#vocab construido por build_vocab.sh
model_dir = "../../data/full/samples" if len(sys.argv) < 2 else sys.argv[1]
out_dir = model_dir if len(sys.argv) < 3 else sys.argv[2]
min_freq = 50 if len(sys.argv) < 4 else int(sys.argv[3])
vocab_fn = model_dir + "/chat_tkn.vocab" if len(sys.argv) < 5 else sys.argv[4]
vocab_freq_fn = out_dir + "/vocab_freq.pkl" if len(sys.argv) < 6 else sys.argv[5]
words_fn = out_dir + "/words.pkl" if len(sys.argv) < 7 else sys.argv[6]


def save_out(vocab_freq, words, vocab_freq_fn, words_fn):
	print("Saving vocab_freq binary on ", vocab_freq_fn)
	with open(vocab_freq_fn, 'wb') as output:
		pickle.dump(vocab_freq, output, pickle.HIGHEST_PROTOCOL)

	print("Saving words binary on ", words_fn)
	with open(words_fn, 'wb') as output:
		pickle.dump(words, output, pickle.HIGHEST_PROTOCOL)


def _build_vocab(vocab_fl, min_freq):
	vocab_freq = dict()
	for line in vocab_fl:
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

	return vocab_freq


def build_words(vocab_freq):
	return sorted(vocab_freq.keys())


def build_vocab(vocab_fn, min_freq, vocab_freq_fn, words_fn):
	with open(vocab_fn, 'r', encoding='utf-8') as vocab_fl:
		vocab_freq = _build_vocab(vocab_fl,min_freq)

	words = build_words(vocab_freq)
	save_out(vocab_freq, words, vocab_freq_fn, words_fn)


before = datetime.datetime.now()
build_vocab(vocab_fn, min_freq, vocab_freq_fn, words_fn)
print("Time elapsed:",datetime.datetime.now()-before)