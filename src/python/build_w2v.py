from nltk.tokenize import TweetTokenizer
from gensim.models import word2vec


class SentenceStream(object):
	def __init__(self, fname):
		self.fname = fname

	def __iter__(self):
		for line in open(self.fname):
			line = ' '.join(TweetTokenizer().tokenize(line))
			yield line.split()





model = word2vec.Word2Vec(SentenceStream('../../chat_corpus.txt'),size=100,window=2,min_count=0,workers=2)

model.save('chat_corpus.w2v')

