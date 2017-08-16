import scipy.sparse
import scipy.io

from sklearn.feature_extraction.text import TfidfVectorizer
from trib_specific.doc_iterator import DocIterator
from trib_specific.bow_iterator import BowDocIterator

import tools.params as params
from tools.params import args,base,vecs
import tools.utils as utils




def build_tfidf_matrix(corpus,min_df,stwords=None):
  
  tfidf_model = TfidfVectorizer(min_df=min_df, stop_words=stwords)
  matrix = tfidf_model.fit_transform(corpus)

  return tfidf_model.get_feature_names(), matrix


def main():
  min_df = int(args.get('min_df', 150))
  timeslice = int(args.get('timeslice', 600))
  champs_fn = args.get("champs", params.data_dir+'base/champs.txt')
  stwords_fn = args.get("stwords", params.data_dir+'base/en_stopwords.txt')
  champs = [champ.strip('\n').strip(' ').lower() for champ in open(champs_fn)]
  stwords = [sw.strip('\n').strip(' ').lower() for sw in open(stwords_fn)] + champs
  
  print("Building tf-idf matrix")
  chat = BowDocIterator(DocIterator(base.chat, base.corpus, timeslice))
  vocab, tfidf_matrix = build_tfidf_matrix(chat, min_df, stwords)
  
  print("Saving results...")  
  utils.save(vecs.tfidf.r2d, chat.row_doc)  
  utils.save(vecs.tfidf.vocab, vocab)
  utils.save(vecs.tfidf.mtx, tfidf_matrix, nparts=vecs.n_matrix)
  

if __name__ == '__main__':
  utils.measure_time(main)
