#vocab <- read.csv('vocab.txt', sep=' ', header = FALSE)

read.csv("chat_offender.csv",sep=',',header=FALSE)
write.csv(chat$V6,sep='',file = "corpus_offender_line.txt",row.names=FALSE,quote=FALSE)
#
#read.csv(neigh_matrix.csv,check.names=FALSE)
#perc.nwords <- t(t(n.words)/rowSums(n.words))
