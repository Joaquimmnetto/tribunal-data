
from pprint import pprint
from gensim.models import LdaMulticore
from gensim.corpora import MmCorpus
from gensim.matutils import Scipy2Corpus
import group_tools
import args_proc as args




def lda_topic_discovery(corpus, id2word, num_topics):
    lda_model = LdaMulticore(corpus=corpus, num_topics=num_topics, id2word=id2word, workers=5)
    return lda_model


def main():
    num_topics = int(args.params.get("num_topics", 15))
    analysis = bool(args.params.get("analysis", False))

    print("Loading bow matrix:")
    spy_mat, id2word = group_tools.load_spy_matrix(args.cnt_team.format(0), args.cnt_team_vocab)
    gsm_corpus = Scipy2Corpus(spy_mat.tocsc())

    print("Making lda model with first matrix:")
    lda_model = lda_topic_discovery(gsm_corpus, id2word, num_topics)
    del spy_mat,gsm_corpus,id2word

    for i in range(1,args.n_matrixes):
        print("Updating model with matrix {0}:".format(i))
        spy_mat = args.load_obj(args.cnt_team.format(i))
        gsm_corpus = Scipy2Corpus(spy_mat.tocsc())
        lda_model.update(gsm_corpus)
        del spy_mat,gsm_corpus
    lda_model.save(args.lda_team)

if __name__ == '__main__':
    args.measure_time(main)
