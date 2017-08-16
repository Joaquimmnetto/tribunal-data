from gensim.models import LdaMulticore, LdaModel, HdpModel
from gensim.matutils import Scipy2Corpus
from gensim.corpora import MmCorpus

import tools.utils as utils
from tools.params import args, vecs, clt




def lda_topic_discovery(corpus, id2word, num_topics, alpha, n_workers):
    if alpha=='auto':
        lda_model = LdaModel(corpus=corpus, minimum_probability=0, alpha=alpha,
                             iterations=100, num_topics=num_topics, id2word=id2word)
    else:
        lda_model = LdaMulticore(corpus=corpus, minimum_probability=0, alpha=alpha,
                             iterations=100, num_topics=num_topics, id2word=id2word, workers=n_workers)    
    return lda_model

def hdp_topic_discovery(corpus, id2word, max_topics):
    hdp_model = HdpModel(corpus=corpus, id2word=id2word, T=max_topics)
    return hdp_model


def main():
    n_workers = int(args.get("n_workers", 3))
    num_topics = int(args.get("num_topics", 15))
    alpha = args.get("alpha", 'symmetric')
    model = args.get("model","lda")

    print("Loading bow matrix:")            
    gsm_corpus = MmCorpus(vecs.bow.mtx.format(0))    

    id2word = utils.load(vecs.bow.vocab)
    id2word = dict([(i, v) for i, v in enumerate(id2word)])
    print("Using",model)
    print("Updating model with matrix 0:")
    if model=='lda':
        topic_model = lda_topic_discovery(gsm_corpus, id2word, num_topics, alpha, n_workers)
    elif model=='hdp':
        topic_model = hdp_topic_discovery(gsm_corpus, id2word, num_topics)
    del gsm_corpus

    for i in range(1, vecs.n_matrix):
        print("Updating model with matrix {0}:".format(i))
        gsm_corpus = MmCorpus(vecs.bow.mtx.format(i))
        topic_model.update(gsm_corpus)
        del gsm_corpus
    
    if model=='lda':
        topic_model.save(clt.lda.model)
    if model=='hdp':
        topic_model.save(clt.hdp.model)

if __name__ == '__main__':
    utils.measure_time(main)
