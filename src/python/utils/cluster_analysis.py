from pprint import pprint
import matplotlib.pyplot as plt
from gensim.models import LdaMulticore

from params import args, clt, vecs
import utils
import numpy as np
import wordcloud


print("Loading inputs")

def save_wordclouds(weights, sufixo=""):
  for l, v in weights:
    wc = wordcloud.WordCloud(max_font_size=250, width=500, height=500, max_words=100,
                             background_color='white').fit_words(v)
    sufixo = ""
    sufixo += str(l) + '_' + "full"
    save_wc(wc, sufixo)


def save_wc(wordcloud, sufixo):
  plt.figure()
  plt.imshow(wordcloud)
  plt.axis("off")
  plt.savefig('wc_' + sufixo + '.png')


def analysis(pp_fn, topic_probs, nwords):
  if not topic_probs:
    print("Aggregating labels count")
    aggr_res = utils.load_obj(pp_fn)
    labels_weight = aggr_res['labels_weight']
    groups_cont = aggr_res['groups_cont']
    topics_sum = aggr_res['topics_sum']
  else:
    print("Getting topics higest-prob. words")
    lda_model = utils.load_obj(clt.lda.model, gensim_class=LdaMulticore)
    labels_weight = utils.topic_words(lda_model, topn_words=nwords)
    groups_cont = []
    topics_sum = dict()

    return labels_weight, groups_cont, topics_sum


def main():
  topic_probs = args.get('topic_probs', 'False') == 'True'
  model_name = args.get('model', 'lda')
  nwords = int(args.get('nwords', 100))
  postprocess_fn = None  
  if model_name=='lda':
    postprocess_fn = clt.lda.postprocess
  elif model_name=='kmn':
    postprocess_fn = clt.kmn.postprocess
    

  labels_weight, groups_cont, topics_sum = analysis(clt.lda.postprocess, topic_probs, nwords)

  print("Applying idf on top", nwords, "words")
  # [(label,[(word,weight),...])]
  if nwords > 0:
    df = utils.load_obj(vecs.df)
    lst_fwords = utils.groups_tfidf(labels_weight, df, num_words=nwords)
  else:
    #
    lst_fwords = [(n, [(w, wht) for w, wht in sorted(ws, key=lambda v: v[1], reverse=True)]) for n, ws in
                  labels_weight.items()]

  #save_wordclouds(lst_fwords, 'topic_prob' if topic_probs else 'bow_sum')
  print("WordClouds saved")
  print("-------------Results----------------")
  print("Top 10 words for each cluster:")
  for gr_lst in lst_fwords:
    print("Cluster", gr_lst[0])
    print([(word, "%.2f" % w) for word, w in gr_lst[1][:10]])

  if not topic_probs:
    print("Cluster/Topic distribution:")
    pprint(groups_cont)

    print("Avg. probability that a doc. belongs to a topic:")
    for topic in topics_sum.keys():
      total = np.sum(topics_sum[topic])
      topics_sum[topic] *= (100.0 / total)

    pprint(topics_sum)


if __name__ == '__main__':
  utils.measure_time(main)
