import gensim.models.word2vec as w2v
import datetime
import sys
corpus = "../../../data/corpus/sample_chat_corpus.crp" if len(sys.argv) < 2 else sys.argv[1]
output = "bin/sample_chat_w2v.bin" if len(sys.argv) < 3 else sys.argv[2]

sentences = w2v.LineSentence(corpus)
#avg sentence size = 5.495 =~ 5.5
print("Building w2v model...")
before = datetime.datetime.now()
model = w2v.Word2Vec(sentences,size=100,window=5,min_count=10,workers=6)
print("Time elapsed:",datetime.datetime.now()-before)

model.save(output)



