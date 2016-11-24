import gensim.models.word2vec as w2v
import datetime
corpus = "../../../data/corpus/offender_tkn.crp"

sentences = w2v.LineSentence(corpus)
#avg sentence size = 5.495 =~ 5.5
print("Building model...")
before = datetime.datetime.now()
model = w2v.Word2Vec(sentences,size=100,window=5,min_count=10,workers=6)
print("Time elapsed:",datetime.datetime.now()-before)

model.save("bin/offender_w2v.bin")



