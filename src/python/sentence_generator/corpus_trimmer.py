# import sys
# import datetime
# import pickle
# from nltk import TweetTokenizer
#
# corpus_fl = "../../corpus_line.txt" if len(sys.argv) < 2 else sys.argv
# ct = 0
# last_ct = 0
#
# with open("words.pkl",'rb') as vf_fl:
# 	vocab_freq = pickle.load(vf_fl)
#
# with open(corpus_fl,'r',encoding='utf-8') as corpus, open("corpus_trimmed.txt",'w',encoding='utf-8') as corpus_trim:
# 	print("Ajusting corpus...")
# 	for line in corpus:
# 		if ct - last_ct > 500000:
# 			print(datetime.datetime.now())
# 			last_ct = ct
# 		ct = ct + 1
#
# 		tk_line = TweetTokenizer(reduce_len=True).tokenize(line.lower())
# 		new_line = []
# 		for token in tk_line:
# 			if token in vocab_freq.keys():
# 				new_line.append(token)
# 		corpus_trim.write(' '.join(new_line)+'\n')
