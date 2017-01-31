import scipy.sparse
import scipy.io
import pickle
import datetime
import nltk

from doc_iterator import DocIterator
from sklearn.feature_extraction.text import CountVectorizer
import args_proc as args

min_freq = int(args.params.get('min_freq', 150))
champs = [champ.strip('\n').strip(' ').lower() for champ in open(args.champs)]
stwords = [sw for sw in open(args.stwords)] + champs
with open(args.words, 'rb') as inp:
	vocab_words = pickle.load(inp)


# vocab_words = [word for word in vocab_words if word not in stwords]


class CountDocIterator(object):
	def __init__(self, doc_iter):
		self.docs = doc_iter
		self.row_doc = dict()

	def __iter__(self):
		stop = False
		index = 0
		for case, match, team, doc in self.docs.next_doc():
			if doc.strip('\n').strip('\t').strip('\r').strip(' ') == '':
				continue

			self.row_doc[index] = (case, match, team)
			index += 1
			yield doc


def build_cnt_matrix(chat_fn, corpus_fn):
	chat = CountDocIterator(DocIterator(chat_fn, corpus_fn))
	cnt_model = CountVectorizer(min_df=min_freq, stop_words=stwords)
	matrix = cnt_model.fit_transform(chat)
	cnt_vocab = cnt_model.get_feature_names()

	return chat.row_doc, cnt_vocab, matrix


def save_outp(row_doc, row_doc_fn, vocab, vocab_fn, matrix, matrix_fn):
	if row_doc is not None:
		with open(row_doc_fn, 'wb') as output:
			print("Saving row_doc")
			pickle.dump(row_doc, output, protocol=2, fix_imports=True)
	if vocab is not None:
		with open(vocab_fn, 'wb') as output:
			print("Saving vocab")
			pickle.dump(vocab, output, protocol=2, fix_imports=True)
	if matrix is not None:
		with open(matrix_fn, 'wb') as output:
			print("Saving matrix")
			scipy.io.mmwrite(output, matrix, field='real', precision=1)


def main():
	before = datetime.datetime.now()
	print("Building counting matrix")
	docs, cnt_vocab, cnt_matrix = build_cnt_matrix(args.chat, args.corpus)
	print("Saving models...")
	save_outp(docs, args.cnt_team_r2d,
	          cnt_vocab, args.cnt_team_vocab,
	          cnt_matrix, args.cnt_team)
	print("Total time elapsed:", datetime.datetime.now() - before)


if __name__ == '__main__':
	main()
