import utils
import mult
import numpy as np

from gensim import LDAMulticore
from params import args,clt,vecs

from concurrent.futures import ProcessPoolExecutor
import pyLDAvis

#  topic_term_dists : array-like, shape (`n_topics`, `n_terms`)
#         Matrix of topic-term probabilities. Where `n_terms` is `len(vocab)`.

#     doc_topic_dists : array-like, shape (`n_docs`, `n_topics`)
#         Matrix of document-topic probabilities.

#     doc_lengths : array-like, shape `n_docs`
#         The length of each document, i.e. the number of words in each document.
#         The order of the numbers should be consistent with the ordering of the
#         docs in `doc_topic_dists`.

#     vocab : array-like, shape `n_terms`
#         List of all the words in the corpus used to train the model.

#     term_frequency : array-like, shape `n_terms`
#         The count of each particular term over the entire corpus. The ordering
#         of these counts should correspond with `vocab` and `topic_term_dists`.



def process_dtd(lda, r2l):
  doc_topic_dist = np.zeros(shape=(len(r2l),lda.num_topics))

  for row in r2l.keys():
    for topic,prob in row:
      doc_topic_dist[row,topic] = prob

  return doc_topic_dist



def process_ttd(lda, ids):  
  if hasattr(lda, 'lda_beta'):
    topic = lda.lda_beta
  else:
    topic = lda.state.get_lambda()
    topic = topic / topic.sum(axis=1)[:, None]
  topic_term_dists = topic[:, ids]
  return topic_term_dists



def process_doclens(bow):
  doc_len = bow.sum(axis=1)
  return doc_len

def main():
  lda = utils.load_obj(clt.lda.model, LDAMulticore)
  r2l = utils.load_obj(clt.lda.r2l)
  vocab = utils.load_obj(vecs.bow.vocab)
  term_frequency = utils.load_obj(vecs.tf)
  n_workers = args.params.get('n_workers',2)
  
  with ProcessPoolExecutor(max_workers=n_workers) as exc:
    dtd_promise = exc.submit(process_dtd,lda,r2l)
    ttd_promise = exc.submit(process_ttd(lda, np.array(range(0,len(vocab)))))
    bow_promises = []  
    for part in range(0, vecs.n_matrix):
      bow = utils.load_obj(vecs.bow.mtx.format(part))
      bow_promises.append(exc.submit(process_doclens, bow))

    doc_topic_dists = dtd_promise.result()
    topic_term_dists = ttd_promise.result()

    doc_lengths = np.array()
    for promise in bow_promises:
      doc_lengths = np.append(doc_lengths,promise.result())

  vis = pyLDAvis.prepare(topic_term_dists, doc_topic_dists, doc_lengths,vocab, term_frequency)

if __name__=='__main__':
  utils.measure_time(main)