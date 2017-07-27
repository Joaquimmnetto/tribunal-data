from params import clt, vecs, args
from gensim.models import Doc2Vec
import utils



def plot_points(d2v_fn,labels_fn):
  d2v = utils.load_obj(d2v_fn, Doc2Vec)
  labels = utils.load_obj(labels_fn)





def main():

  labels = utils.load_obj(clt.kmn.labels)


  for index,labels in enumerate(labels):
    doc = r2d[index]




  pass





if __name__ == "__main__":
  utils.measure_time(main)