import warnings
warnings.filterwarnings("ignore")

import utils
import numpy as np

from gensim.models import HdpModel
from params import args,clt,vecs

from concurrent.futures import ProcessPoolExecutor
import pyLDAvis
#pyLDAvis params:
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



def process_dtd(lda, r2l_fn):
  print("processing dtd")
  r2l_len = sum([len(utils.load_obj(r2l_fn.format(i))) for i in range(0,vecs.n_matrix)])
  doc_topic_dist = np.zeros(shape=(r2l_len, lda.num_topics))
  print("dtd matrix allocated:",doc_topic_dist.shape) 
  for part in range(0,vecs.n_matrix):
    r2l = utils.load_obj(r2l_fn.format(part))    
    for row in r2l.keys():
      for topic,prob in enumerate(r2l[row]):
        doc_topic_dist[row,topic] = prob

  return doc_topic_dist



def process_ttd(model, ids):  
  print("processing ttd")
  #Case HDP:
  if hasattr(model, 'lda_beta'):
    topic = model.lda_beta
  else:
    topic = model.state.get_lambda()
    topic = topic / topic.sum(axis=1)[:, None]
  topic_term_dists = topic[:, ids]
  return topic_term_dists



def process_doclens(bow):
  print("Processing doclen")
  doc_len = bow.sum(axis=1)
  tfs = bow.sum(axis=0)
  return doc_len, tfs

def main():
  model = args.get("model","lda")
  
  if model == 'lda':
    model = utils.load_obj(clt.lda.model, LdaMulticore)  
  elif model == 'hdp':
    model = utils.load_obj(clt.hdp.model, HdpModel)  

  
  vocab = utils.load_obj(vecs.bow.vocab)  
  n_workers = int(args.get('n_workers',3))

  with ProcessPoolExecutor(max_workers=n_workers) as exc:
    print('queue ttd')
    ttd_promise = exc.submit(process_ttd, model, np.array(range(0,len(vocab))))
    bow_promises = []  
    
    print('queue matrixes')
    for part in range(0, vecs.n_matrix):
      bow = utils.load_obj(vecs.bow.mtx.format(part))
      bow_promises.append(exc.submit(process_doclens, bow))

    print('processing results')    
    topic_term_dists = ttd_promise.result()
    doc_lengths = []
    term_frequency = None    
    for promise in bow_promises:
      dl,freqs = promise.result()
      doc_lengths = np.append(doc_lengths, dl)
      
      if term_frequency is None:
        term_frequency = freqs
      else:
        term_frequency = term_frequency + freqs
         
  print('process dtd')
  doc_topic_dists = process_dtd(lda,clt.lda.r2l if model=='lda' else clt.hdp.r2l)
  term_frequency = np.array(term_frequency)[0]
  
  print(term_frequency)
  print('processing vis')
  vis = pyLDAvis.prepare(topic_term_dists, doc_topic_dists, doc_lengths, vocab, term_frequency)
  pyLDAvis.save_html(vis, 'vis.html')
  pyLDAvis.save_json(vis, 'vis.json')

if __name__=='__main__':
  utils.measure_time(main)
