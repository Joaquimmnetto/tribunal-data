from gensim.models import LdaMulticore
from gensim.matutils import Scipy2Corpus
from gensim.corpora import MmCorpus

import utils
#import args_proc as args
from params import args, vecs, clt




def lda_topic_discovery(corpus, id2word, num_topics):
    lda_model = LdaMulticore(corpus=corpus, minimum_probability=0, num_topics=num_topics, id2word=id2word, workers=5)
    return lda_model


def main():
    num_topics = int(args.get("num_topics", 15))
    analysis = bool(args.get("analysis", False))

    print("Loading bow matrix:")        
    gsm_corpus = MmCorpus(vecs.bow.mtx.format(0))    
    id2word = utils.load_obj(vecs.bow.vocab)

    id2word = dict([(i, v) for i, v in enumerate(id2word)])

    print("Updating model with matrix 0:")
    lda_model = lda_topic_discovery(gsm_corpus, id2word, num_topics)
    del gsm_corpus

    for i in range(1, vecs.n_matrix):
        print("Updating model with matrix {0}:".format(i))
        #spy_mat = utils.load_obj(vecs.bow.mtx.format(i))
        #gsm_corpus = Scipy2Corpus(spy_mat.tocsc())
        gsm_corpus = MmCorpus(vecs.bow.mtx.format(i))
        lda_model.update(gsm_corpus)
        del gsm_corpus
    
    lda_model.save(clt.lda.model)

if __name__ == '__main__':
    utils.measure_time(main)
