from pprint import pprint
import matplotlib.pyplot as plt
from gensim.models import LdaMulticore
from gensim.matutils import sparse2full
from gensim.corpora import MmCorpus
import args_proc as args
import numpy as np
import wordcloud

import group_tools

print("Loading inputs")


def save_wordclouds(weights, sufixo=""):
  for l, v in weights:
    wc = wordcloud.WordCloud(max_font_size=250, width=500, height=500, max_words=100,
                             background_color='white').fit_words(v)
    sufixo = ""
    sufixo += str(l) + '_' + args.current_model
    save_wc(wc, sufixo)


def save_wc(wordcloud, sufixo):
  plt.figure()
  plt.imshow(wordcloud)
  plt.axis("off")
  plt.savefig('wc_' + sufixo + '.png')


def main():
  topic = args.params.get('topic', 'arguments')
  nwords = int(args.params.get('nwords', 100))

  print("Aggregating labels count")
  aggr_res = args.load_obj(args.aggr_lda_teams)
  teams_weight = aggr_res['labels_weight']
  labels_weight = {'ally': teams_weight['ally'][topic],
                   'enemy': teams_weight['enemy'][topic],
                   'offender': teams_weight['offender'][topic]
                   }

  teams_cont = aggr_res['topics_sum']  # 'topics_count',mas tá erado no pkl atual
  groups_cont = {'ally': teams_cont['ally'][topic],
                 'enemy': teams_cont['enemy'][topic],
                 'offender': teams_cont['offender'][topic]
                 }

  print("Applying idf on top", nwords, "words")
  # [(label,[(word,weight),...])]
  if nwords > 0:
    lst_fwords = group_tools.groups_idf(labels_weight, num_words=nwords)
  else:
    lst_fwords = [(n, [(w, wht) for w, wht in sorted(ws, key=lambda v: v[1], reverse=True)]) for n, ws in
                  labels_weight.items()]

  save_wordclouds(lst_fwords, topic + '_bow_sum')
  print("WordClouds saved")
  print("-------------Results----------------")
  print('For topic', topic)
  print("Top 10 words for each group:")
  for gr_lst in lst_fwords:
    print("Team", gr_lst[0])
    # print([(word,"%.2f"%w) for word,w in gr_lst[1][:10]])
    print([word for word, w in gr_lst[1][:10]])
  print("Group distribution for ths topic:")
  total = sum(groups_cont.values())
  pprint([(group, "%.3f%%" % (c * 100 / total)) for group, c in groups_cont.items()])


if __name__ == '__main__':
  args.measure_time(main)
