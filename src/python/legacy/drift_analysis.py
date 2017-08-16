import tools.params
from tools.params import base,args,clt,vecs
import tools.utils as utils
import count_matrix_builder as bow_builder

from gensim.models import LdaMulticore
from gensim.matutils import Scipy2Corpus





def main():
  params.load_model_dir( "model_drift/")
  params.load_names()

  timeslice_size = int(args.get('timeslice_size', 600))
  min_freq = int(args.get('min_freq', 800))

  row2lab = list()

  print("Loading bow matrix with timeslices")
  
  lda = utils.load(clt.lda.model, LdaMulticore)

  lda_vocab = { v:k for k,v in lda.id2word.items()}
  
  row2doc, bow_vocab, bow_matrix = bow_builder.build_cnt_matrix(base.chat,
                                                                base.corpus,
                                                                _min_freq=min_freq,
                                                                _timeslice=timeslice_size,
                                                                vocab=lda_vocab
                                                                )
  print(len(lda.id2word), bow_matrix.shape)
    
  gsm_corpus = Scipy2Corpus(bow_matrix)  
  print("Labeling docs...")
  for row in gsm_corpus:
    topics = lda[row]
    first_topic = sorted(topics, key=lambda x: x[1], reverse=True)[0][0]
    row2lab.append(first_topic)

  utils.save(vecs.bow.r2d, row2doc)
  utils.save(clt.lda.r2l, row2lab)


if __name__ == '__main__':
  utils.measure_time(main)
