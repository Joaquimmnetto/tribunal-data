import sys
import datetime
import pickle
import scipy.sparse
import scipy.io

import args_proc as args


def create_neigh(words, corpus):
  ct = 0
  last_ct = 0

  vocab_len = len(words)
  print("Vocab size:", vocab_len)

  print("Alocando Matriz...")
  neigh = scipy.sparse.coo_matrix((vocab_len, vocab_len)).todok()

  first_words = set()
  w_indexes = dict((w, i) for i, w in enumerate(words))

  print('Preenchendo Matriz...')
  for line in corpus:
    if ct - last_ct > 1000000:
      print(datetime.datetime.now())
      last_ct = ct
    ct = ct + 1

    # tk_line = TweetTokenizer(reduce_len=True).tokenize(line.lower())
    tk_line = line.replace('\n', '').split(sep=" ")
    # print(tk_line)
    for i, token in enumerate(tk_line[:len(tk_line) - 1]):
      next_w = tk_line[i + 1]
      try:
        w_index = w_indexes[token]
        n_index = w_indexes[next_w]

        if i == 0:
          first_words.add(token)
        neigh[w_index, n_index] += 1
      except KeyError:
        pass

  return neigh, first_words


def save_matrices(neigh, first_words, neigh_fl, fwords_fl):
  with open(neigh_fl, 'wb') as output:
    # file object
    scipy.io.mmwrite(output, neigh.tocsr())

  with open(fwords_fl, 'wb') as output:
    # object file
    pickle.dump(first_words, output, pickle.HIGHEST_PROTOCOL)


# -----------------------------------------------------------------
print("Carregando Vocabuário from ", args.words)
with open(args.words, 'rb') as wr_fl:
  _words = pickle.load(wr_fl)

with open(args.corpus, 'r', encoding='utf-8') as _corpus:
  neigh, first_words = create_neigh(_words, _corpus)

save_matrices(neigh, first_words, args.neigh, first_words)
