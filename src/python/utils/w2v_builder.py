# import gensim.models.word2vec as w2v
# import datetime
# import sys
# #import args_proc as args
#
# min_freq = int(args.params.get('min_freq', 150))
#
#
# def build_w2v(corpus, min_freq):
#   sentences = w2v.LineSentence(corpus)
#   # avg sentence size = 5.495 =~ 5.5
#   model = w2v.Word2Vec(sentences, size=100, window=5, min_count=min_freq, workers=6)
#
#   return model
#
#
# before = datetime.datetime.now()
# model = build_w2v(args.corpus, min_freq)
# model.save(args.w2v)
# print("Time elapsed:", datetime.datetime.now() - before)
