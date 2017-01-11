import scipy.sparse
import scipy.io
import sys
import pickle
import datetime

import nltk.corpus
from gensim.matutils import MmReader
from gensim.models import TfidfModel
from sklearn.feature_extraction.text import TfidfVectorizer
from count_matrix_builder import DocIterator



model_dir ="../../../data/full" if len(sys.argv) < 3 else sys.argv[2]
out_dir = model_dir if len(sys.argv) < 4 else sys.argv[3]

chat_fn = model_dir+"/chat.csv" if len(sys.argv) < 5 else sys.argv[4]
corpus_fn = model_dir+"/chat_tkn.crp" if len(sys.argv) < 6 else sys.argv[5]
matches_fn = model_dir+"/matches.csv" if len(sys.argv) < 7 else sys.argv[6]
words_fn = model_dir+"/words.pkl" if len(sys.argv) < 8 else sys.argv[7]

stwords = nltk.corpus.stopwords.words("english")

with open(words_fn,'rb') as inp:
	vocab_words = pickle.load(inp)
	vocab_words = [word for word in vocab_words if word not in stwords]


def build_tfidf_matrix(chat_fn, corpus_fn):

	chat = DocIterator(chat_fn,corpus_fn)
	tfidf_model = TfidfVectorizer(stop_words = stwords, min_df = 50, vocabulary = vocab_words)
	matrix = tfidf_model.fit_transform(chat)

	return chat.get_docs(), matrix


def build_tfidf_gs_model(cnt_matrix_fn):
	cnt_matrix_gs = MmReader(cnt_matrix_fn)
	tfidf_model = TfidfModel(cnt_matrix_gs)
	return tfidf_model


def save_outp(docs, tfidf_matrix):
	if docs is not None:
		with open(out_dir + "/match_index.pkl", 'wb') as output:
			# object file
			pickle.dump(docs, output, pickle.HIGHEST_PROTOCOL)
	if tfidf_matrix is not None:
		with open(out_dir+"/tfidf_matrix.mm", 'wb') as output:
			# file object
			scipy.io.mmwrite(output, tfidf_matrix)


before = datetime.datetime.now()
print("Building tf-idf matrix")
docs, tfidf_matrix = build_tfidf_matrix(chat_fn, corpus_fn)
save_outp(docs,tfidf_matrix)
print("Subtotal time elapsed:",datetime.datetime.now()-before)
