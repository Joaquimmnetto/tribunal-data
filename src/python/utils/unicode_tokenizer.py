import sys
from nltk.tokenize import TweetTokenizer
fl = sys.argv[1]


with open(fl,'r') as corpus:
	tkn = TweetTokenizer(preserve_case=False)
	for line in corpus:
		tokenized = tkn.tokenize(line)
		print(' '.join(tokenized))



