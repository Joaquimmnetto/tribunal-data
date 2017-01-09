import sys
import collections
import csv

model_dir ="../../data/full" if len(sys.argv) < 2 else sys.argv[1]
out_dir ="../../data/full" if len(sys.argv) < 3 else sys.argv[2]

min_count = 50 if len(sys.argv) < 4 else sys.argv[3]

chat_fn = model_dir+"/sample/chat.csv" if len(sys.argv) < 4 else sys.argv[3]
#words_fn = model_dir+"/sample/words.pkl" if len(sys.argv) < 5 else sys.argv[4]

TeamLog = collections.namedtuple('TeamLog',['case','match','team','vector'])
docs = {'ally':list(), 'enemy':list(), 'offender':list()}



def team2tfidf(chat_fn):
	with open(chat_fn,'r') as inp:
		csv_rd = csv.reader(inp)

	case = 0
	match = 0
	chats = {'ally': list(), 'enemy': list(), 'offender': list()}
	for row in csv_rd:
		next_case = int(row[0])
		next_match = int(row[1])
		team = row[2]

		if case != next_case or match != next_match:
			corpus_ally  = ' '.join(chats['ally'])
			docs['ally'].append(TeamLog(case,match,'ally',))






def team2skipgram(chat_fn):
	pass


def docs2csv():
	pass

def docs2bin():
	#gensim .save() method
	pass
