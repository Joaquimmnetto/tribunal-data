
from gensim.corpora import Dictionary
from trib_specific.doc_iterator import DocIterator
from trib_specific.bow_iterator import CountDocIterator

from utils import utils
from utils.params import args, base, vecs

class GensimCorpus:
  def __init__(self, gsm_dict, corpus):
    self.gsm_dict = gsm_dict
    self.corpus = corpus

  def __iter__(self):
    for doc in self.corpus:
      yield self.gsm_dict.doc2bow(doc)

#1.200.000 is 5% of the document total (24.000.000) for tribunaldb
def build_dict(corpus, lower_cut=1200000, upper_cut=0.75, vocab_trim=20000):
  id2word = Dictionary(corpus)
  if lower_cut is not None or upper_cut is not None:
    id2word.filter_extremes(no_below=lower_cut, no_above=upper_cut, keep_n=vocab_trim)

  return id2word

def main():  
  timeslice = int(args.get('timeslice', 600))

  gsm_dict = build_dict(CountDocIterator(DocIterator(base.chat, base.corpus, timeslice),gensim=True),
                        lower_cut=1200000, upper_cut=0.75, vocab_trim=20000)

  gsm_dict.save(vecs.bow.vocab) 
  
  corpus = CountDocIterator(DocIterator(base.chat, base.corpus, timeslice),gensim=True)  
  MmCorpus.serialize(vecs.bow.mtx, corpus = GensimCorpus(gsm_dict, corpus))
  utils.save_obj(vecs.bow.r2d, corpus.row_doc)
  

if __name__ == '__main__':
  utils.measure_time(main)