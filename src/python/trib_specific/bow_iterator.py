

class BowDocIterator(object):
  def __init__(self, doc_iter, gensim=False):
    self.docs_iter = doc_iter
    self.row_doc = dict()
    self.gensim = gensim

  def __iter__(self):    
    index = 0
    for case, match, team, docs in self.docs_iter.next_doc():
      for timeslice, doc in enumerate(docs):
        if doc.strip('\n').strip('\t').strip('\r').strip(' ') == '':
          continue
        self.row_doc[index] = (case, match, team, timeslice)
        index += 1
        
        if not self.gensim:
          yield doc
        else:
          yield doc.split()