import sys
import datetime
import csv
from nltk.tokenize import TweetTokenizer

corpus_fl = "../../corpus_line.txt" if len(sys.argv) < 2 else sys.argv[1]
next_csv = "../../next_matrix.csv" if len(sys.argv) < 3 else sys.argv[2]

ct = 0
last_ct = 0

neigh = dict()
vocab_freq = dict()

print('Contruindo Matriz...')
with open(corpus_fl,'r',encoding='utf-8') as corpus:
	for line in corpus:
		if ct - last_ct > 500000:
			print(datetime.datetime.now())
			last_ct = ct
		ct = ct+1
		tk_line = TweetTokenizer(reduce_len=True).tokenize(line.lower())
		for i,token in enumerate(tk_line[:len(tk_line)-1]):
			next = tk_line[i+1]
			if token not in neigh.keys():
				neigh[token] = dict()
				vocab_freq[token] = 0

			if next not in neigh[token]:
				neigh[token][next] = 0
			vocab_freq[token] +=1
			neigh[token][next] += 1

to_remove = []
print('Full vocab. size:',len(vocab_freq))
for word,freq in vocab_freq.items():
	if freq < 50:
		to_remove.append(word)

for word in to_remove:
	del vocab_freq[word]


words = sorted(vocab_freq.keys())
print("Trimmed Vocab size:",len(words))

ct = 0
last_ct = 0

print('Salvando Matriz')
with open(next_csv,'w',encoding='utf-8') as csvfl:
	csv_wr = csv.writer(csvfl)
	csv_wr.writerow(words)

	for extword in words:
		if ct - last_ct > 500:
			print(datetime.datetime.now())
			last_ct = ct
		ct = ct + 1

		dict_row = neigh[extword]
		row_keys = sorted(dict_row.keys())
		row = list()
		for word in words:
			if word in row_keys:
				row.append(dict_row[word])
			else:
				row.append(0)

		csv_wr.writerow(row)
		del row








