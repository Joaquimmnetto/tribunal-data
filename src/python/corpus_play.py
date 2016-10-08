#-*- coding: utf-8 -*-

import nltk

from nltk.corpus import stopwords

stopwords = stopwords.words('english')
corpus_fl = open('chat_corpus.txt','rb')
tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
corpus = []
for line in corpus_fl:
	ln = [w.lower() for w in tokenizer.tokenize(line)]
	corpus += ln


fdist = nltk.FreqDist(corpus)

print '\n'.join([str((word,count)) for word,count in fdist.most_common() if word not in stopwords][:500])




english_vocab = set(w.lower() for w in nltk.corpus.words.words())

corpus_vocab = set(corpus) - set(stopwords)

corp_eng_diff = corpus_vocab - english_vocab

#92% das palavras não são inglês padrão. NOVENTA E DOIS!
print float(len(corp_eng_diff))/len(corpus_vocab)


#print corp_eng_diff



