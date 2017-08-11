import sys
from collections import namedtuple


args = dict()

model_dir = ""

def read_args(argv):
  for arg in argv:
    key_val = arg.split(':')
    args[key_val[0]] = key_val[1]
  print(args)

def load_arg(arg, fname, _dir=model_dir):
  if arg not in args.keys():
    default_val = _dir+"/"+fname
    args[arg] = default_val
  return args[arg]

# def load_model_dir(directory):
#   model_dir = directory
#   sys.path.append(directory)
#   return directory


def load_names(bdir, mdir):

  base = namedtuple("base", ['chat', 'corpus'])(
    chat=load_arg('chat', "chat_parsed.csv",_dir=bdir),
    corpus=load_arg('corpus', "chat_tkn.crp", _dir=bdir)
  )

  _matrix_t = namedtuple("Matrix", ["mtx", "r2d", "vocab"])
  vecs = namedtuple("matrixes",['bow','tfidf','d2v','df','n_matrix'])(

      bow = _matrix_t(
        mtx = load_arg('bow_mtx', 'bow_{0}.mtx', mdir),
        r2d = load_arg('bow_r2d', "bow_r2d.pkl", mdir),
        vocab = load_arg("bow_vocab", 'bow_vocab.pkl', mdir)
      ),
      tfidf = _matrix_t(
        mtx = load_arg('tfidf_mtx', 'tfidf_{0}.mtx', mdir),
        r2d = load_arg('tfidf_r2d', "tfidf_r2d.pkl", mdir),
        vocab = load_arg("tfidf_vocab", 'tfidf_vocab.pkl', mdir)
      ),
      d2v = _matrix_t(
        mtx = load_arg('d2v_model', 'd2v_model.bin', mdir),
        r2d = load_arg('d2v_r2l', 'd2v_r2d.pkl', mdir),
        vocab = load_arg('d2v_vocab', 'd2v_vocab.pkl', mdir)
      ),

      n_matrix = args.get("n_matrix", 5),
      df = load_arg('df', 'df.pkl', bdir)
  )


  _model_t = namedtuple("Model",["model", "labels", "r2l", "postprocess"])
  clt = namedtuple("clt", ["kmn", "lda", 'hdp'])(
    kmn = _model_t(
        model=load_arg('kmn_model', 'kmn_centres.pkl', mdir),
        labels=load_arg('kmn_labels', 'kmn_labels.pkl', mdir),
        r2l=load_arg('kmn_r2l', 'kmn_r2l.pkl', mdir),
        postprocess=load_arg('kmn_pp', 'kmn_pp.pkl', mdir)
      ),
      lda = _model_t(
        model=load_arg('lda_model', "lda_model.gsm", mdir),
        labels=load_arg('lda_labels', 'lda_labels.pkl', mdir),
        r2l=load_arg('lda_r2l', 'lda_r2l_{0}.pkl', mdir),
        postprocess=load_arg('lda_pp', 'lda_pp.pkl', mdir)
      ),
      hdp = _model_t(
        model=load_arg('hdp_model', "hdp_model.gsm", mdir),
        labels=load_arg('hdp_labels', 'hdp_labels.pkl', mdir),
        r2l=load_arg('hdp_r2l', 'hdp_r2l_{0}.pkl', mdir),
        postprocess=load_arg('hdp_pp', 'hdp_pp.pkl', mdir)
      )
  )

  return base,vecs,clt

  

if len(sys.argv) > 1:
  read_args(sys.argv[1:])

data_dir = "../../../data/"

base_dir = args.get("base_dir", "../../../data/base/samples")
model_dir = args.get("model_dir", "../../../data/model_drift/samples")
print("Model dir:{0}",model_dir)
base,vecs,clt = load_names(base_dir, model_dir)

# Ideias:
# Bigramas
# stemming?
# Tirar nomes dos champions
# Modificar o número de tópicos? Como definir um numero bom de tópicos?
