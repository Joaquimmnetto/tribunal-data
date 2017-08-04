from gensim.corpora import MmCorpus

class BowGensimIterator:


  def __init__(self,*files):
    self.mm_corpora = []
    for file in files:
      self.mm_corpora.append(MmCorpus(file))

  def __iter__(self):
    for corpus in self.mm_corpora:
      yield corpus.__iter__()