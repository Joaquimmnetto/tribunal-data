require(Matrix)
require(slam)
require(Matrix.utils)
require(tm)
require(ldatuning)
require(data.table)

pkl2R <- function(pkl_fn){
  library(rPython)
  python.exec("import pickle")
  python.exec(paste("obj = pickle.load(open(",pkl_fn,",'rb'))"))
  return(python.get('obj'))
}

mm_tdm = "data/full/samples/count_team.mtx"
vocab = "'data/full/samples/count_team_vocab.pkl'"
labels = "'data/full/samples/kmn_labels_4.pkl'"

cnt <- readMM(mm_tdm)
vocab <- pkl2R(vocab)
labels <- pkl2R(labels)

#cnt <- cbind(cnt,labels)

colnames(cnt) <- vocab
rownames(cnt) <- labels

cnt <- simple_triplet_matrix(cnt)

rowsum(cnt, row.names(cnt))
#z<- aggregate.Matrix(cnt, by = list(cnt$labels__), FUN = 'sum')




