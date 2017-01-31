import args_proc as args


def calc_idfs(cnt_matrix):
	dfs = cnt_matrix.sum(axis=0)
	idfs = 1.0/dfs
	return idfs

def asdict(idfs,id2word):
	return dict([(id2word[i], idf) for i, idf in enumerate(idfs.tolist()[0])])


def main():
	print("Calculating idfs...")
	idfs = calc_idfs(args.load_obj(args.cnt_team))
	print("Saving idfs...")
	args.save_pkl(args.idf_team, asdict(idfs, args.load_obj(args.cnt_team_vocab)))


if __name__ == '__main__':
	args.measure_time(main)
