import sys
import pickle
import datetime

model_dir = "../../../data/full/samples" if len(sys.argv) < 2 else sys.argv[1]
out_dir = model_dir if len(sys.argv) < 3 else sys.argv[2]

corpus_fn = model_dir+"/chat_tkn.crp" if len(sys.argv) < 4 else sys.argv[3]
correct_pkl = model_dir+"/corrector_dict.pkl" if len(sys.argv) < 5 else sys.argv[4]
out_fn = out_dir+"/chat_corrected.crp" if len(sys.argv) < 6 else sys.argv[5]


def correct_errors(corpus_fn, correct_pkl, out_fn):

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


begin_time = datetime.datetime.now()
correct_errors(corpus_fn, correct_pkl, out_fn)
print("Time Elapsed:",datetime.datetime.now()-begin_time)

