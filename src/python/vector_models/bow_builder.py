import scipy.sparse
import scipy.io
import numpy as np
import math
from gensim.corpora import Dictionary, MmCorpus

from sklearn.feature_extraction.text import CountVectorizer

from trib_specific.doc_iterator import DocIterator
from trib_specific.bow_iterator import BowDocIterator
from tools.calculate_df import process_df

import tools.utils as utils
from tools.utils import GensimCorpus

import tools.params as params
from tools.params import args, vecs, base


def build_dict(corpus, lower_cut=None, upper_cut=None, vocab_trim=20000):
  id2word = Dictionary(corpus)
  if lower_cut is not None or upper_cut is not None:
    id2word.filter_extremes(no_below=lower_cut, no_above=upper_cut, keep_n=vocab_trim)
    id2word.compactify()
  bow_vocab = [id2word[id] for id in sorted(id2word.keys())]    
  return id2word, bow_vocab

def build_bow_skl(corpus, stop_words, min_df, max_df = 1.0, vocab=None):
  bow_model = CountVectorizer(min_df=min_df, max_df=max_df, stop_words=stop_words, vocabulary=vocab)
  matrix = bow_model.fit_transform(corpus)
  bow_vocab = bow_model.get_feature_names()
    
  return bow_vocab, matrix


def main():
  min_df = float(args.get('min_df', 240000)) #240.000 is 1% of the document total (24.000.000) for tribunaldb. 
  min_df = int(min_df) if min_df > 1.0 else min_df  #gensim only accepts full count value for this, sklearn accepts percentage(in [0.0,1.0]) also
  max_df = float(args.get('max_df', 0.9)) #90%~95% para considerar stopword é um valor comum na literatura
  timeslice = int(args.get('timeslice', 600))
  gensim = args.get('gensim',"False") == "True"

  champs_fn = args.get("champs", params.data_dir+'base/champs.txt')
  stwords_fn = args.get("stwords", params.data_dir+'base/en_stopwords.txt')
  champs = [champ.strip('\n').strip(' ').lower() for champ in open(champs_fn)]
  stwords = [sw.strip('\n').strip(' ').lower() for sw in open(stwords_fn)] + champs

  freq = None  
  chat = BowDocIterator(DocIterator(base.chat, base.corpus, timeslice),gensim)
  if gensim:
    print("Building gensim dict")
    gsm_dict, bow_vocab = build_dict(chat,lower_cut=min_df, upper_cut=max_df, vocab_trim=20000)    
    
    print("Serializing results")
    corpus = BowDocIterator(DocIterator(base.chat, base.corpus, timeslice),gensim=True)         
    MmCorpus.serialize(vecs.bow.mtx, corpus = GensimCorpus(gsm_dict, corpus), progress_cnt=100000)    
    print("Loading full matrix")
    bow_matrix = utils.load(vecs.bow.mtx).tocsr()
  else:
    print("Building scipy matrix")    
    bow_vocab, bow_matrix = build_bow_skl(chat, stop_words=stwords, min_df=min_df)      
  
  print("Calculating wf")
  freq = bow_matrix.sum(axis=0)
  freq = np.array(freq)[0] 

  print("Saving results...")
  utils.save(vecs.df, freq)
  utils.save(vecs.bow.r2d, chat.row_doc)  
  utils.save(vecs.bow.vocab, bow_vocab)
  utils.save(vecs.bow.mtx, bow_matrix, nparts=vecs.n_matrix)
  

if __name__ == '__main__':
  utils.measure_time(main)
