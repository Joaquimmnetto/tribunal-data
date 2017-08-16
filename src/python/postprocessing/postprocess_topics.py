import numpy as np

import tools.utils as utils
from gensim.matutils import sparse2full
from concurrent.futures import ProcessPoolExecutor
from tools.params import vecs,clt,args



def postprocess(vocab, part):  
  print("Starting part ",part)  
 
  bow_mtx = utils.load(vecs.bow.mtx.format(part)).tocsr()  
  r2l = utils.load(clt.lda.r2l.format(part))
  print("Files lodaded for part",part)
  row = part * bow_mtx.shape[0]
  labels = range(0, r2l[row].shape[0])
  labels_sum = dict([(label, np.zeros(len(vocab))) for label in labels])
  topics_sum = dict([(label, np.zeros(len(labels))) for label in labels])
  topics_count = dict([(label, 0) for label in labels])
  
  
  for bow in bow_mtx:
    topics = r2l[row]
    first_topic = np.argmax(topics)    
    labels_sum[first_topic] += np.asarray(bow.todense())[0]
    topics_sum[first_topic] += topics
    topics_count[first_topic] += 1
    row += 1
    
  return labels_sum, topics_sum, topics_count

def instance_or_update(src_dict,new_dict):
  if src_dict is None:
    src_dict = new_dict
  else:
    src_dict.update(new_dict)
  
  return src_dict

def main():

  n_workers = int(args.get("n_workers", 2))
  vocab = utils.load(vecs.bow.vocab)

  labels_sum = None
  topics_sum = None
  topics_count = None

  promises = list()
  
  with ProcessPoolExecutor(max_workers=n_workers) as exc:
    for part in range(0,vecs.n_matrix):
      promise = exc.submit(postprocess, vocab, part)
      promises.append(promise)

    print("Starting workers")  
    for promise in promises:
      ls, ts, tc = promise.result()
      
      labels_sum = instance_or_update(labels_sum, ls)
      topics_sum = instance_or_update(topics_sum, ts)
      topics_count = instance_or_update(topics_count, tc)

  
  for label, vec in labels_sum.items():
    labels_sum[label] = sorted(list(zip(vocab, vec)), key=lambda x: x[1], reverse=True)
  
  mat_len = sum(topics_count.values())
  for label in topics_sum.keys():
    topics_count[label] /= float(mat_len)
  
  res = {"model": 'lda', "labels_weight": labels_sum, "topics_sum": topics_sum, "groups_cont": topics_count}
  utils.save(clt.lda.postprocess, res)

if __name__=="__main__":
  utils.measure_time(main)
