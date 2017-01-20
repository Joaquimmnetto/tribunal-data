require(Matrix)
require(tm)
require(ldatuning)

pkl2R <- function(pkl_fn){
  library(rPython)
  
  python.exec("import pickle")
  python.exec(paste("obj = pickle.load(open(",pkl_vocab,",'rb'))"))
  return(python.get('obj'))
}

mm_tdm = "data/full/samples/bigrams/count_team.mm"
pkl_vocab = "'data/full/samples/bigrams/count_team_vocab.pkl'"

tdm <- readMM(mm_tdm)




tdm <- as.DocumentTermMatrix(tdm,weighting=weightTf)

vocab = pkl2R(pkl_vocab)
colnames(tdm) <- vocab
#remover linhas vazias(soma == 0)
result <- FindTopicsNumber(tdm, topics = seq(from=2,to=20,by=1),
                           metrics = c("Griffiths2004", "CaoJuan2009", "Arun2010", "Deveaud2014"),
                           method = "Gibbs",
                           mc.cores = 3L,
                           verbose = TRUE)


