import sys
import pickle
import datetime
import csv
import nltk.corpus


model_dir ="../../../data/full" if len(sys.argv) < 3 else sys.argv[2]
out_dir = model_dir if len(sys.argv) < 4 else sys.argv[3]

chat_fn = model_dir+"/chat.csv" if len(sys.argv) < 5 else sys.argv[4]
corpus_fn = model_dir+"/chat_tkn.crp" if len(sys.argv) < 6 else sys.argv[5]
words_fn = model_dir+"/words.pkl" if len(sys.argv) < 8 else sys.argv[7]

stwords = nltk.corpus.stopwords.words("english")

docs_file = open(out_dir+'/chat_by_team.csv', 'a')

with open(words_fn,'rb') as inp:
	vocab_words = pickle.load(inp)
	vocab_words = [word for word in vocab_words if word not in stwords]


def build_file(case, match, chats):
	chat_to_file(case, match, 'ally', chats['ally'])
	chat_to_file(case, match, 'enemy', chats['enemy'])
	chat_to_file(case, match, 'offender', chats['offender'])


def chat_to_file(case, match, team, content):
	csv_wr = csv.writer(docs_file)
	chat_text = ' '.join(content)
	csv_wr.writerow([case, match, team, chat_text])


before = datetime.datetime.now()
