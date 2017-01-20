import sys
import datetime

params = dict()


def load_dir(arg, folder, sample):
	module = sys.modules[__name__]
	default_val = data_dir + "/" + folder + "/samples" if sample else data_dir + "/" + folder
	value = params.get(arg, default_val)

	setattr(module, arg, value)

	return getattr(module, arg, value)


def load_arg(arg, fname):
	module = sys.modules[__name__]
	default_val = model_dir + "/" + fname
	value = params.get(arg, default_val)

	setattr(module, arg, value)

	return getattr(module, arg, value)


def read_args(argv):
	for arg in argv:
		print(arg)
		key_val = arg.split(':')
		params[key_val[0]] = key_val[1]
		print(params)

def bigrams(fn):
	folders = fn.split('/')
	folders.insert(len(folders)-1,'bigrams')
	return '/'.join(folders)


# ---------------------------------------------------------
if len(sys.argv) > 1:
	read_args(sys.argv[1:])

data_dir = "../../../data"
model_dir = load_dir('model_dir', "full", sample=True)
out_dir = params.get('out_dir', model_dir)

# csvs base
chat = load_arg('chat', "chat.csv")
players = load_arg('players', "players.csv")
matches = load_arg('matches', "matches.csv")

# modelos basicos de vocabulário
corpus = load_arg('corpus', "chat_tkn.crp")
vocab_csv = load_arg('vocab_csv', "chat_tkn.vocab")
vocab = load_arg('vocab', "vocab_freq.pkl")
words = load_arg('words', "words.pkl")

# modelos de word vectors
# w2v
w2v = load_arg('w2v', "w2v_model.bin")
# d2v
d2v_team = load_arg('d2v_team', 'd2v_team.bin')
d2v_team_r2d = load_arg('d2v_team_r2d', "d2v_team_r2d.pkl")
# bow(matriz de contagem)
cnt_team = load_arg('cnt_team', 'count_team.mtx')
cnt_team_r2d = load_arg('cnt_team_r2d', "cnt_team_r2d.pkl")
cnt_team_vocab = load_arg('cnt_team_vocab', 'count_team_vocab.pkl')
# tfidf
tfidf_team = load_arg('tfidf_team', "tfidf_team.mtx")
tfidf_team_r2d = load_arg('tfidf_team_r2d', "tfidf_team_r2d.pkl")
tfidf_team_vocab = load_arg('tfidf_team_vocab', 'tfidf_team_vocab.pkl')

#topic models
lda_team = load_arg('lda_team',"lda_teams.gsm")
lda_team_csv = load_arg('lda_team_csv',"lda_teams.csv")

#LSI pode ser usado como um redutor de dimensionalidade sobre o tfidf, por isso a matriz.
lsi_team_model = load_arg('lsi_team_model','lsi_teams.gsm')
lsi_team_csv = load_arg('lsi_team_csv','lsi_teams.csv')
lsi_team_matrix = load_arg('lsi_team_matrix','lsi_teams.mtx')

hdp_team = load_arg('hdp_team',"hdp_teams.gsm")
hdp_team_csv = load_arg('hdp_team_csv',"hdp_teams.csv")

# outputs do corretor
corr = load_arg('corr', "corrector_dict.pkl")
err = load_arg('err', "error_dict.pkl")

# modelos do gerador de palavras
neigh = load_arg('neigh', "neigh.spy")
fwords = load_arg('fwords', "first_words.pkl")

#Ideias:
#Bigramas
#Tirar nomes dos champions
#Modificar o número de tópicos? Como definir um numero bom de tópicos?

def measure_time(main):
	before = datetime.datetime.now()
	main()
	print("Time elapsed:", datetime.datetime.now() - before)

