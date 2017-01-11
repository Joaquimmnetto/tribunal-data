import scipy.sparse
import scipy.io
import sys
import pickle
import datetime
import csv
import nltk.corpus

from sklearn.feature_extraction.text import CountVectorizer


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


class DocIterator(object):

	def __init__(self, chat_fn, corpus_fn):
		self.chat_fn = chat_fn
		self.corpus_fn = corpus_fn
		self.docs = dict()


	def __iter__(self):
		i = 0
		with open(self.chat_fn) as cht, open(self.corpus_fn) as crp:
			csv_rd = csv.reader(cht)
			case = 0
			match = 0
			doc_num = 0
			chats = {'ally': list(), 'enemy': list(), 'offender': list()}


			for row, crp_line in zip(csv_rd, crp):
				i+=1
				next_case = int(row[0])
				next_match = int(row[1])
				team = row[2]
				if team.strip() == '':
					continue

				if next_case != case or next_match != match:
					if case != 0:
						yield ' '.join(chats['ally'])
						yield ' '.join(chats['enemy'])
						yield ' '.join(chats['offender'])

						doc_num = build_docs(case, match, self.docs, doc_num)

					del chats
					chats = {'ally': list(), 'enemy': list(), 'offender': list()}
					match = next_match
					case = next_case

				chats[team].append(crp_line)

	def get_docs(self):
		return self.docs


def build_cnt_matrix(chat_fn, corpus_fn):
	chat = DocIterator(chat_fn,corpus_fn)
	cnt_model = CountVectorizer(stop_words = stwords, min_df = 50, vocabulary = vocab_words)
	matrix = cnt_model.fit_transform(chat)

	return chat.get_docs(), matrix


def build_docs(case, match, docs, doc_num):
	docs[doc_num] = (match, case, 'ally')
	doc_num += 1
	docs[doc_num] = (match, case, 'enemy')
	doc_num += 1
	docs[doc_num] = (match, case, 'offender')
	doc_num += 1
	return doc_num


def save_outp(docs, cnt_matrix):
	if cnt_matrix is not None:
		with open(out_dir+"/count_matrix.mm", 'wb') as output:
			# file object
			scipy.io.mmwrite(output, cnt_matrix)
	if docs is not None:
		with open(out_dir + "/match_index.pkl", 'wb') as output:
			# object file
			pickle.dump(docs, output, pickle.HIGHEST_PROTOCOL)


def main():
	before = datetime.datetime.now()
	print("Building counting matrix")
	docs, cnt_matrix = build_cnt_matrix(chat_fn, corpus_fn)
	save_outp(docs, cnt_matrix)
	print("Total time elapsed:", datetime.datetime.now() - before)


if __name__ == '__main__':
	main()


