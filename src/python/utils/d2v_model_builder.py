import datetime
from gensim.models.doc2vec import TaggedDocument, Doc2Vec
from doc_iterator import DocIterator

from params import args_, vecs, base
import utils


class D2VDocIterator(object):
  def __init__(self, docIter):
    self.docs_iter = docIter
    self.row_doc = dict()

  def __iter__(self):
    index = 0
    for case, match, team, docs in self.docs_iter.next_doc():
      for timeslice, doc in enumerate(docs):
        if doc.strip('\n').strip('\t').strip('\r').strip(' ') == '':
          continue

        tg_doc = TaggedDocument(words=doc.split(' '), tags=[index])
        self.row_doc[index] = (case, match, team, timeslice)
        index += 1
        yield tg_doc


def build_d2v_model(chat_fn, corpus_fn, min_freq):
  docs = D2VDocIterator(DocIterator(chat_fn, corpus_fn))
  model = Doc2Vec(docs, size=100, workers=6, min_count=min_freq)
  return docs.row_doc, model


def save_outp(d2v_model, row_doc):
  d2v_model.save(vecs.d2v.model)
  utils.save_pkl(vecs.d2v.r2d, row_doc)


def main():
  min_freq = int(args_.get('min_freq', 5))
  before = datetime.datetime.now()

  print("Building d2v model")
  row_doc, d2v_model = build_d2v_model(base.chat, base.corpus, min_freq)
  print("Subtotal time elapsed:", datetime.datetime.now() - before)
  print("Saving models...")
  save_outp(d2v_model, row_doc)


if __name__ == '__main__':
  utils.measure_time(main)
