require(data.table)
pkl2R <- function(pkl_fn){
  library(rPython)
  python.exec("import pickle")
  python.exec(paste("obj = pickle.load(open(",pkl_fn,",'rb'))"))
  return(python.get('obj'))
}


labels <- pkl2R("'data/full/samples/lda_labels_4.pkl'")
r2d <- pkl2R("'data/full/samples/cnt_team_r2d.pkl'")

labels <- cbind(as.data.table(t(matrix(unlist(r2d), nrow=length(unlist(r2d[1]))))),as.data.table(labels))
rm(r2d)

names(labels) <- c("case","match","relation.offender","group")



