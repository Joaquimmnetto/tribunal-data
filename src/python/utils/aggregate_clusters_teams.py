from gensim.matutils import sparse2full
from gensim.corpora import MmCorpus
import numpy as np
import args_proc as args
import csv


def load_topics(fname):
  res = dict()
  csv_rd = csv.reader(open(fname))
  for row in csv_rd:
    case = int(row[0])
    match = int(row[1])
    res[(case, match, 'ally')] = row[2]
    res[(case, match, 'enemy')] = row[3]
    res[(case, match, 'offender')] = row[4]

  return res


def summarize_topics_team(bow_mat_fn, vocab_fn):
  bow_mat = MmCorpus(bow_mat_fn)
  vocab = args.load_obj(vocab_fn)
  r2d = args.load_obj(args.cnt_team_r2d)
  match_topic = load_topics(args.group_labels_lda)

  labels_sum = {'ally': dict(), 'enemy': dict(), 'offender': dict()}
  topics_count = {'ally': dict(), 'enemy': dict(), 'offender': dict()}
  x = 0
  for i, bow in enumerate(bow_mat):
    doc_id = r2d[i]
    team = doc_id[2]
    try:
      topic = match_topic[doc_id]
    except KeyError:
      x += 1
      pass
    try:
      labels_sum[team][topic] += sparse2full(bow, len(vocab))
    except KeyError:
      labels_sum[team][topic] = np.zeros(len(vocab))

    try:
      topics_count[team][topic] += 1
    except KeyError:
      topics_count[team][topic] = 0

  del bow_mat

  for team, team_dict in labels_sum.items():
    for topic, vec in team_dict.items():
      labels_sum[team][topic] = sorted(list(zip(vocab, vec)), key=lambda x: x[1], reverse=True)

  print(x)
  return labels_sum, topics_count


def main():
  lda = args.params.get('lda', 'True') == 'True'

  print("Loading labels count")
  if lda:
    labels_sum, topics_count = summarize_topics_team(args.cnt_team, args.cnt_team_vocab)
    res = {"lda": True, "labels_weight": labels_sum, "topics_count": topics_count}
    args.save_pkl(args.aggr_lda_teams, res)


if __name__ == '__main__':
  args.measure_time(main)
