import sys
from collections import namedtuple


args_ = dict()

model_dir = ""

def read_args(argv):
  for arg in argv:
    key_val = arg.split(':')
    args_[key_val[0]] = key_val[1]
  print(args_)

def load_arg(arg, fname, _dir=model_dir):
  if arg not in args_.keys():
    default_val = _dir+"/"+fname
    args_[arg] = default_val
  return args_[arg]

def load_model_dir(directory):
  global model_dir
  if model_dir in sys.path:
    sys.path.remove(model_dir)

  model_dir = directory
  sys.path.append(directory)
  return directory

def load_names():

  base = namedtuple("base", ['chat', 'corpus'])(
    chat=load_arg('chat', "chat_parsed.csv",dir=base_dir),
    corpus=load_arg('corpus', "chat_tkn.crp", dir=base_dir)
  )

  _matrix_t = namedtuple("Matrix", ["mtx", "r2d", "vocab"])
  matrixes = namedtuple("matrixes",['bow','tfidf','d2v','df','n_matrix'])(

      bow = _matrix_t(
        mtx = load_arg('bow_mtx', 'bow_{0}.mtx'),
        r2d = load_arg('bow_r2d', "bow_r2d.pkl"),
        vocab = load_arg("bow_vocab", 'bow_vocab.pkl')
      ),
      tfidf = _matrix_t(
        mtx = load_arg('tfidf_mtx', 'tfidf_{0}.mtx'),
        r2d = load_arg('tfidf_r2d', "tfidf_r2d.pkl"),
        vocab = load_arg("tfidf_vocab", 'tfidf_vocab.pkl')
      ),
      d2v = _matrix_t(
        mtx = load_arg('d2v_model', 'd2v_model.bin'),
        r2d = load_arg('d2v_r2l', 'd2v_r2d.pkl'),
        vocab = load_arg('d2v_vocab', 'd2v_vocab.pkl')
      ),

      n_matrix = args_.get("n_matrix", 5),
      df = load_arg('df', 'df.pkl')
  )


  _model_t = namedtuple("Model",["model", "labels", "r2l", "postprocess"])
  clustering = namedtuple("clt", ["kmn", "lda"])(
    kmn = _model_t(
        model=load_arg('kmn_model', 'kmn_model.bin'),
        labels=load_arg('kmn_labels', 'kmn_labels.pkl'),
        r2l=load_arg('kmn_r2l', 'kmn_r2l.pkl'),
        postprocess=load_arg('kmn_pp', 'kmn_pp.pkl')
      ),
      lda = _model_t(
        model=load_arg('lda_model', "lda_model.gsm"),
        labels=load_arg('lda_labels', 'lda_labels.pkl'),
        r2l=load_arg('lda_r2l', 'lda_r2l.pkl'),
        postprocess=load_arg('lda_pp', 'lda_pp.pkl')
      )
  )

  return base,matrixes,clustering


if len(sys.argv) > 1:
  read_args(sys.argv[1:])

sys.path.append("../../../data/")

base_dir = args_.get("base_dir", "../../../data/base/samples/")
model_dir = load_model_dir(args_.get("model_dir", "../../../data/full/samples/"))
print("Model dir:{0}",model_dir)

base, vecs, clt = load_names()




# modelos basicos de vocabulário

#vocab_csv = load_arg('vocab_csv', "chat_tkn.vocab")

#words = load_arg('words', "words.pkl")
#chat_parsed = load_arg('chat_parsed', "chat_parsed.csv")


# Ideias:
# Bigramas
# stemming?
# Tirar nomes dos champions
# Modificar o número de tópicos? Como definir um numero bom de tópicos?
