import gensim.models.word2vec as w2v
import datetime
corpus = "../../../cht_tokenized.txt"

sentences = w2v.LineSentence(corpus)

print("Building model...")
before = datetime.datetime.now()
model = w2v.Word2Vec(sentences,size=100,window=5,min_count=20,workers=2)
print("Time elapsed:",datetime.datetime.now()-before)

model.save("bin/corpus_w2v.bin")



