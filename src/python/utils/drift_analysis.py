import args_proc as args
import count_matrix_builder as bow_builder

from gensim.models import LdaMulticore
from gensim.matutils import Scipy2Corpus





def main():

  model_drift = "model_drift/"
  timeslice_size = int(args.params.get('timeslice_size', 600))
  min_freq = int(args.params.get('min_freq', 800))
  lda_model = args.params.get('lda_model',
                              model_drift + "lda_drift.gsm")

  row2lab = list()

  print("Loading bow matrix with timeslices")
  
  lda = args.load_obj(model_drift + "lda_drift.gsm",LdaMulticore)
  lda_vocab = { v:k for k,v in lda.id2word.items() }   
  
  row2doc, bow_vocab, bow_matrix = bow_builder.build_cnt_matrix(args.chat_parsed,
                                                                args.corpus,
                                                                _min_freq=min_freq,
                                                                _timeslice=timeslice_size,
                                                                vocab=lda_vocab
                                                                )
  print(len(lda.id2word), bow_matrix.shape)
  
  bow_builder.save_outp(row2doc,model_drift+"row2doc.pkl",
                         bow_vocab,model_drift+"bow_vocab.pkl",
                         bow_matrix, model_drift+"bow_drift_{0}.mm")

  
  gsm_corpus = Scipy2Corpus(bow_matrix)
  
  print("Labeling docs...")
  for row in gsm_corpus:
    topics = lda[row]
    first_topic = sorted(topics, key=lambda x: x[1], reverse=True)[0][0]
    row2lab.append(first_topic)

  args.save_pkl(model_drift + "cnt_drift_r2d.pkl", row2doc)
  args.save_pkl(model_drift + "lda_drift_row2lab.pkl", row2lab)


if __name__ == '__main__':
  args.measure_time(main)
