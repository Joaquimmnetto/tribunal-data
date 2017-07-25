import pickle
import sys
import datetime
import scipy.io

params = dict()


def load_model(arg, folder, sample):
  module = sys.modules[__name__]
  default_val = data_dir + '/' + folder + "/samples" if sample else data_dir + '/' + folder
  value = params.get(arg, default_val)

  setattr(module, arg, value)
  current_model = value.replace('/', '') + ("_samples" if 'sample' in value else "")
  return getattr(module, arg, value), current_model


def load_arg(arg, fname):
  module = sys.modules[__name__]
  default_val = model_dir + "/" + fname
  value = params.get(arg, default_val)

  setattr(module, arg, value)

  return getattr(module, arg, value)


def read_args(argv):
  for arg in argv:
    key_val = arg.split(':')
    params[key_val[0]] = key_val[1]
  print(params)


def bigrams(fn):
  folders = fn.split('/')
  folders.insert(len(folders) - 1, 'bigrams')
  return '/'.join(folders)


# ---------------------------------------------------------
if len(sys.argv) > 1:
  read_args(sys.argv[1:])

n_matrixes = 5
#timeslice_size = 10 * 60  # 10 min
data_dir = "../../../data"
sys.path.append(data_dir)

model_dir, current_model = load_model('model_dir', "full", sample=False)
print(model_dir)
out_dir = params.get('out_dir', model_dir)

champs = 'champs.txt'
stwords = 'en_stopwords.txt'
# csvs base
chat = load_arg('chat', "chat.csv")
players = load_arg('players', "players.csv")
matches = load_arg('matches', "matches.csv")

# modelos basicos de vocabulário
corpus = load_arg('corpus', "chat_tkn.crp")
vocab_csv = load_arg('vocab_csv', "chat_tkn.vocab")
vocab = load_arg('vocab', "vocab_freq.pkl")
words = load_arg('words', "words.pkl")
chat_parsed = load_arg('chat_parsed', "chat_parsed.csv")

# modelos de word vectors
# w2v
w2v = load_arg('w2v', "w2v_model.bin")
# d2v
d2v_team = load_arg('d2v_team', 'd2v_team.bin')
d2v_team_r2d = load_arg('d2v_team_r2d', "d2v_team_r2d.pkl")
# bow(matriz de contagem)
cnt_team = load_arg('cnt_team', 'count_team_{0}.mtx')
cnt_team_r2d = load_arg('cnt_team_r2d', "cnt_team_r2d.pkl")
cnt_time_r2d = load_arg('cnt_time_r2d', "cnt_time_r2d.pkl")
cnt_team_vocab = load_arg('cnt_team_vocab', 'count_team_vocab.pkl')
cnt_time_vocab = load_arg('cnt_time_vocab', 'count_time_vocab.pkl')
idf = load_arg('idf', 'idf.pkl')
# tfidf
tfidf_team = load_arg('tfidf_team', "tfidf_team.mtx")
tfidf_team_r2d = load_arg('tfidf_team_r2d', "tfidf_team_r2d.pkl")
tfidf_team_vocab = load_arg('tfidf_team_vocab', 'tfidf_team_vocab.pkl')

# topic models
lda_team = load_arg('lda_team', "lda_teams.gsm")
lda_time = load_arg('lda_time', "lda_time.gsm")
lda_team_csv = load_arg('lda_team_csv', "lda_teams.csv")

# LSI pode ser usado como um redutor de dimensionalidade sobre o tfidf, por isso a matriz.
lsi_team_model = load_arg('lsi_team_model', 'lsi_teams_{0].gsm')
lsi_team_csv = load_arg('lsi_team_csv', 'lsi_teams_{0}.csv')
lsi_team_matrix = load_arg('lsi_team_matrix', 'lsi_teams_{0}.mtx')

# modelo de tópico que não precisa de parâmetros. Parece ser bem recente.
# hierarquical dirchlet process
hdp_team = load_arg('hdp_team', "hdp_teams.gsm")
hdp_team_csv = load_arg('hdp_team_csv', "hdp_teams.csv")

kmn_team_labels = load_arg('kmn_team_labels', 'kmn_labels_{0}.pkl')
aggr_kmn = load_arg('aggr_kmn_{0}', "aggr_kmn_{0}.pkl")

lda_team_labels = load_arg('lda_team_labels', 'lda_labels_{0}.pkl')
aggr_lda = load_arg('aggr_lda', "aggr_lda.pkl")

aggr_lda_time = load_arg('aggr_lda_time', "aggr_lda_time.pkl")
lda_time_labels = load_arg('lda_time_labels', 'lda_time_labels.pkl')

group_labels_lda = load_arg('group_labels_lda', 'group_labels_lda.csv')
aggr_lda_teams = load_arg('aggr_lda_teams', 'aggr_lda_teams.pkl')

# outputs do corretorexit
corr = load_arg('corr', "corrector_dict.pkl")
err = load_arg('err', "error_dict.pkl")

# modelos do gerador de palavras
neigh = load_arg('neigh', "neigh.spy")
fwords = load_arg('fwords', "first_words.pkl")


# Ideias:
# Bigramas
# stemming?
# Tirar nomes dos champions
# Modificar o número de tópicos? Como definir um numero bom de tópicos?


def measure_time(main):
  before = datetime.datetime.now()
  main()
  print("Time elapsed:", datetime.datetime.now() - before)


def save_pkl(fname, obj):
  pickle.dump(obj, open(fname, 'wb'), protocol=2, fix_imports=True)


def load_obj(fname, gensim_class=None):
  if fname.endswith('.pkl'):
    return pickle.load(open(fname, 'rb'))
  if fname.endswith('.mtx') or fname.endswith('.mm'):
    return scipy.io.mmread(fname)
  if fname.endswith('.gsm') or fname.endswith('.bin'):
    return gensim_class.load(fname)
