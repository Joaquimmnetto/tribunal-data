from gensim.corpora import MmCorpus
from gensim.corpora import IndexedCorpus

class BowGensimIterator(IndexedCorpus):


  def __init__(self, files):
    IndexedCorpus.__init__(self,list(files)[0])
    self.mm_corpora = []
    for file in files:
      self.mm_corpora.append(MmCorpus(file))

  def __iter__(self):
    print(self.mm_corpora)
    for corpus in self.mm_corpora:
      for value in corpus:
          yield value

  def __len__(self):
      return sum([len(corpus) for corpus in self.mm_corpora])
