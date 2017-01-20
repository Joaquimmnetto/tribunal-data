
import pickle
import datetime
from gensim.models.doc2vec import TaggedDocument,Doc2Vec
from count_matrix_builder import DocIterator

import args_proc as args

min_freq = int(args.params.get('min_freq',150))

class D2VDocIterator(object):
	def __init__(self,docIter):
		self.docs = docIter
		self.row_doc = dict()

	def __iter__(self):
		stop = False
		index = 0
		for case, match, team, doc in self.docs.next_doc():
			tg_doc = TaggedDocument(words=doc.split(' '),tags = [index])
			self.row_doc[index] = (case, match, team)
			index += 1
			yield tg_doc


def build_d2v_model(chat_fn,corpus_fn):
	docs = D2VDocIterator(DocIterator(chat_fn,corpus_fn))
	model = Doc2Vec( docs, size=100, workers=6, min_count=min_freq)
	return docs.row_doc, model

def save_outp(d2v_model,row_doc):
	d2v_model.save(args.d2v_team)

	with open(args.d2v_team_r2d,'wb') as output:
		# object file
		pickle.dump(row_doc, output, pickle.HIGHEST_PROTOCOL)

def main():
	before = datetime.datetime.now()
	print("Building d2v model")
	row_doc, d2v_model = build_d2v_model(args.chat,args.corpus)
	print("Subtotal time elapsed:", datetime.datetime.now() - before)
	print("Saving models...")
	save_outp(d2v_model,row_doc)
	print("Total time elapsed:", datetime.datetime.now() - before)


if __name__ == '__main__':
	main()


