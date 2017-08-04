from gensim.models import LdaMulticore
from gensim.matutils import Scipy2Corpus

from corpus_iterator import BowGensimIterator
import utils
#import args_proc as args
from params import args, vecs, clt




def lda_topic_discovery(corpus, id2word, num_topics):
    lda_model = LdaMulticore(corpus=corpus, num_topics=num_topics, id2word=id2word, workers=5)
    return lda_model


def main():
    num_topics = int(args.get("num_topics", 15))
    analysis = bool(args.get("analysis", False))

    print("Loading bow matrix:")    
    bow_names = (vecs.bow.mtx.format(i) for i in range(0,vecs.n_matrix))
    gsm_corpus = BowGensimIterator(*bow_names)    
    id2word = load_obj(vocab)
    id2word = dict([(i, v) for i, v in enumerate(id2word))

    print("Making lda model with first matrix:")
    lda_model = lda_topic_discovery(gsm_corpus, id2word, num_topics)
    del spy_mat,gsm_corpus,id2word

    # for i in range(1, vecs.n_matrix):
    #     print("Updating model with matrix {0}:".format(i))
    #     spy_mat = utils.load_obj(vecs.bow.mtx.format(i))
    #     gsm_corpus = Scipy2Corpus(spy_mat.tocsc())
    #     lda_model.update(gsm_corpus)
    #     del spy_mat,gsm_corpus
    
    lda_model.save(clt.lda.model)

if __name__ == '__main__':
    utils.measure_time(main)
