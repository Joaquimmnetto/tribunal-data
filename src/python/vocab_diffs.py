import sys
import pickle
import csv
import math

def load_pkl(fname):
	with open(fname, "rb") as inp:
		return pickle.load(inp)

model_dir ="../../data" if len(sys.argv) < 2 else sys.argv[1]
out_dir ="../../data" if len(sys.argv) < 3 else sys.argv[2]

ally_vocab_fn = model_dir+"/ally/samples/vocab_freq.pkl" if len(sys.argv) < 4 else sys.argv[3]
enemy_vocab_fn = model_dir+"/enemy/samples/vocab_freq.pkl" if len(sys.argv) < 5 else sys.argv[4]
offender_vocab_fn = model_dir+"/offender/samples/vocab_freq.pkl" if len(sys.argv) < 6 else sys.argv[5]

ally_vocab = load_pkl(ally_vocab_fn)
enemy_vocab = load_pkl(enemy_vocab_fn)
offender_vocab = load_pkl(offender_vocab_fn)


def build_vocab_diffs(ally_vocab, enemy_vocab, offender_vocab):
	df_ae = dict()
	df_ao = dict()
	df_eo = dict()
	all_words = set(ally_vocab.keys()) | set(enemy_vocab.keys()) | set(offender_vocab.keys())

	for word in all_words:
		ally_cnt = math.floor(ally_vocab.get(word, 0) / 4)
		enemy_cnt = math.floor(enemy_vocab.get(word, 0) / 5)
		offender_cnt = math.floor(offender_vocab.get(word, 0))

		df_ae[word] = ally_cnt - enemy_cnt
		df_ao[word] = ally_cnt - offender_cnt
		df_eo[word] = enemy_cnt - offender_cnt

	return df_ae,df_ao,df_eo

def save_diff(fl,diff):
	csv_wr = csv.writer(fl)
	for word,count in diff.items():
		csv_wr.writerow([word,count])


def save_vocab_diffs(df_ae, df_ao, df_eo):
	with open(out_dir+"/df_ae.csv",'w') as output:
		save_diff(output,df_ae)

	with open(out_dir+"/df_ao.csv",'w') as output:
		save_diff(output,df_ao)

	with open(out_dir+"/df_eo.csv",'w') as output:
		save_diff(output,df_eo)

df_ae,df_ao,df_eo = build_vocab_diffs(ally_vocab,enemy_vocab,offender_vocab)

save_vocab_diffs(df_ae,df_ao,df_eo)

