import sys
import pickle
import datetime

corpus_fn = "../../../src/shell/out/chat_full_tkn.crp" if len(sys.argv) < 2 else sys.argv[1]
correct_pkl = "../../../src/shell/out/chat_full_correct.pkl" if len(sys.argv) < 4 else sys.argv[3]
out_fn = "chat_full_corrected.crp" if len(sys.argv) < 5 else sys.argv[4]


begin_time = datetime.datetime.now()
with open(correct_pkl,'rb') as inp:
	correction = pickle.load(inp)

with open(corpus_fn,'r') as corpus_fl:
	with open(out_fn,'w') as out_fl:
		for line in corpus_fl:
			for word in line.split(' '):
				try:
					right = correction[word]
				except KeyError:
					right = word
				out_fl.write(right)
				out_fl.write(" ")
			
		out_fl.write("\n")

print("Time Elapsed:",datetime.datetime.now()-begin_time)

