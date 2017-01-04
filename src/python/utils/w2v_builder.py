import gensim.models.word2vec as w2v
import datetime
import sys

model_dir = "../../data/full/samples" if len(sys.argv) < 2 else sys.argv[1]
out_dir = model_dir if len(sys.argv) < 3 else sys.argv[2]
min_cnt = 50 if len(sys.argv) < 4 else int(sys.argv[3])

corpus = model_dir+"/chat_tkn.crp" if len(sys.argv) < 5 else sys.argv[4]
output = out_dir+"/w2v_model.bin" if len(sys.argv) < 6 else sys.argv[5]



def build_w2v(corpus,min_cnt):
	sentences = w2v.LineSentence(corpus)
	#avg sentence size = 5.495 =~ 5.5

	model = w2v.Word2Vec(sentences,size=100,window=5,min_count=min_cnt,workers=6)

	return model


before = datetime.datetime.now()
model = build_w2v(corpus,min_cnt)
model.save(output)
print("Time elapsed:",datetime.datetime.now()-before)