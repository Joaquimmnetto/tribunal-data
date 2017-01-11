import sys
import collections
import csv
import nltk
import gensim
import pickle


model_dir ="../../data/full/samples" if len(sys.argv) < 2 else sys.argv[1]
out_dir ="../../data/full/samples" if len(sys.argv) < 3 else sys.argv[2]

min_count = 50 if len(sys.argv) < 4 else sys.argv[3]

chat_fn = model_dir+"/sample/chat.csv" if len(sys.argv) < 4 else sys.argv[3]
words_fn = model_dir+"/sample/vocab_freq.pkl" if len(sys.argv) < 5 else sys.argv[4]

TeamLog = collections.namedtuple('TeamLog',['case','match','vector'])
docs = list()

with open(words_fn,'rb') as inp:
	words = pickle.load(inp)

class ChatIterator(object):

	def __init__(self,chat_fn):
		self.chat_fn = chat_fn
		with open(self.chat_fn, 'r') as inp:
			csv_rd = csv.reader(inp)
			self.gendict = gensim.corpora.Dictionary(row[5].split() for row in csv_rd)
			self.gendict.filter_tokens(
				[self.gendict.token2id[word] for word in words if word in self.gendict.token2id]
			)
			self.gendict.compactify()


	def __iter__(self):
		with open(self.chat_fn, 'r') as inp:
			csv_rd = csv.reader(inp)
			case = 0
			match = 0
			chats = list()
			for row in csv_rd:
				next_case = int(row[0])
				next_match = int(row[1])

				if next_case != case or next_match != match:
					if case != 0:
						docs.append( (case,match) )
						yield self.gendict.doc2bow(' '.join(chats))

					match = next_match
					case = next_case
					chats.clear()

				chat = row[5]
				chats.append(chat)




def make_logs(docs,tfidf_model,corpus):
	logs = list()
	for i,vec in enumerate(tfidf_model[corpus]):
		logs.append( TeamLog(docs[0],docs[1],vec) )


def save_csv(teams_vecs):
	pass


def save_bin(teams_vecs):
	pass


def team2tfidf(chat_fn,docs):
	corpus = ChatIterator(chat_fn)
	tfidf_model = gensim.models.TfidfModel(corpus)
	teams_vecs = make_logs(docs,tfidf_model,corpus)
	save_csv(team_vecs)
	save_bin(team_vecs)

def team2skipgram(chat_fn):
	pass


def docs2csv():
	pass

def docs2bin():
	#gensim .save() method
	pass
