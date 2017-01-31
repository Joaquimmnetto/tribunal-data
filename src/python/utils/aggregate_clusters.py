from gensim.models import LdaMulticore
from gensim.matutils import sparse2full
from gensim.corpora import MmCorpus
import numpy as np
import args_proc as args


def summarize_topic_labels(bow_mat_fn, vocab_fn):
	bow_mat = MmCorpus(bow_mat_fn)
	vocab = args.load_obj(vocab_fn)
	lda_model = args.load_obj(args.lda_team, gensim_class=LdaMulticore)

	labels = range(0, lda_model.num_topics)

	labels_sum = dict([(label, np.zeros(len(vocab))) for label in labels])
	topics_sum = dict([(label, np.zeros(len(labels))) for label in labels])
	topics_count = dict([(label, 0) for label in labels])
	for i, bow in enumerate(bow_mat):
		topics = lda_model[bow]

		first_topic = sorted(topics, key=lambda x:x[1], reverse=True)[0][0]
		labels_sum[first_topic] += sparse2full(bow, len(vocab))
		topics_sum[first_topic] += sparse2full(topics, lda_model.num_topics)
		topics_count[first_topic] += 1
	del bow_mat

	mat_len = sum(topics_count.values())

	for label, vec in labels_sum.items():
		labels_sum[label] = sorted(list(zip(vocab, vec)), key=lambda x: x[1], reverse=True)

	for label in topics_sum.keys():
		topics_count[label] /= float(mat_len)

	return labels_sum, topics_sum, topics_count


def summarize_cluster_labels(bow_mat_fn, n_clusters, vocab_fn):
	bow_mat = MmCorpus(bow_mat_fn)
	vocab = args.load_obj(vocab_fn)

	labels = args.load_obj(args.team_labels.format(n_clusters))

	which_labels, counts = np.unique(labels, return_counts=True)

	labels_sum = dict([(label, len(vocab)) for label in which_labels])
	for i, bow in enumerate(bow_mat):
		labels_sum[labels[i]] += sparse2full(bow, len(vocab))
	del bow_mat

	for label, vec in labels_sum.items():
		labels_sum[label] = sorted(list(zip(vocab, vec)), key=lambda x: x[1], reverse=True)

	return labels_sum, counts


def main():
	lda = args.params.get('lda', 'True') == 'True'
	n_groups = int(args.params.get('n_groups', 4))

	print("Aggregating labels count")
	if lda:
		labels_weight, topics_sum, groups_cont = summarize_topic_labels(args.cnt_team, args.cnt_team_vocab)
		res = {"lda":True, "labels_weight":labels_weight, "topics_sum":topics_sum, "groups_cont":groups_cont}
		args.save_pkl(args.aggr_lda.format(n_groups), res)
	else:
		labels_weight, groups_cont = summarize_cluster_labels(args.cnt_team, n_groups, args.cnt_team_vocab)
		res = {"lda":False, "labels_weight": labels_weight, "groups_cont": groups_cont}
		args.save_pkl(args.aggr_kmn.format(n_groups), res)


if __name__ == '__main__':
	args.measure_time(main)