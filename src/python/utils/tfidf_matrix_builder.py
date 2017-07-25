import scipy.sparse
import scipy.io

from sklearn.feature_extraction.text import TfidfVectorizer
from doc_iterator import DocIterator
from count_matrix_builder import CountDocIterator
import count_matrix_builder

import args_proc as args

min_freq = int(args.params.get('min_freq', 150))


def build_tfidf_matrix(chat_fn, corpus_fn):
  chat = CountDocIterator(DocIterator(chat_fn, corpus_fn))
  tfidf_model = TfidfVectorizer(min_df=min_freq, stop_words=count_matrix_builder.stwords)
  matrix = tfidf_model.fit_transform(chat)

  return chat.row_doc, tfidf_model.get_feature_names(), matrix


def main():
  print("Building tf-idf matrix")
  docs, vocab, tfidf_matrix = build_tfidf_matrix(args.chat, args.corpus)
  print("Saving models...")
  count_matrix_builder.save_outp(row_doc=docs, row_doc_fn=args.tfidf_team_r2d,
                                 vocab=vocab, vocab_fn=args.tfidf_team_vocab,
                                 matrix=None, matrix_fn=None)
  scipy.io.mmwrite(args.tfidf_team, tfidf_matrix, field='real', precision=4)


if __name__ == '__main__':
  args.measure_time(main)
