require(data.table)
require(wordcloud)
require(tm)
require(dplyr)
require(dtplyr)

out.wc.dir <- 'imgs/diff/wordclouds'
out.table.dir <- 'imgs/diff/tables'

save_wc <- function(vocab,fname){
  wordcloud(vocab$word, vocab$diff, max.words=150, random.order=FALSE,scale=c(4,0.9))
  dest_fl <- paste(out.wc.dir,'/',fname,'.png',sep='')
  dev.print(png,dest_fl,width=800,height=600)
  dev.off()
}

save_table <- function(vocab,fname,n){
  grid.table(vocab[1:n])
  dest_fl <- paste(out.table.dir,'/',fname,'.png',sep='')
  dev.print(png,dest_fl,width=200,height=600)
  dev.off()
}

save_plots <- function(vocab,fname,n=20){
  save_wc(vocab,fname)
  save_table(vocab,fname,n)
}

pp <- function(dt, stwords){
  dt <- dt[!(word %in% stwords)]
  rev_dt <- dt %>% mutate(diff = -1*diff)
  dt <- dt[diff > 0][order(-diff)]
  rev_dt <- rev_dt[diff > 0][order(-diff)]
  
  
  return(list(dt=dt,rdt=rev_dt))
  
}

df.ae <- setDT(fread("data/full_df_ae.csv",header=FALSE,showProgress=TRUE))
df.ao <- setDT(fread("data/full_df_ao.csv",header=FALSE,showProgress=TRUE))
df.eo <- setDT(fread("data/full_df_eo.csv",header=FALSE,showProgress=TRUE))
rows <- c("word","diff")
setnames(df.ae, names(df.ae),rows)
setnames(df.ao, names(df.ao),rows)
setnames(df.eo, names(df.eo),rows)

stwords <- append(stopwords("english"),c('u','im','ur'))
res <- pp(df.ae, stwords)
df.ae <- res$dt
df.ea <- res$rdt
res <- pp(df.ao, stwords)
df.ao <- res$dt
df.oa <- res$rdt
res <- pp(df.eo, stwords)
df.eo <- res$dt
df.oe <- res$rdt


nfirst = 30
save_plots(df.ae,'ally-enemy',nfirst)
save_plots(df.ao,'ally-offender',nfirst) 
save_plots(df.ea,'enemy-ally',nfirst)
save_plots(df.eo,'enemy-offender',nfirst)
save_plots(df.oa,'offender-ally',nfirst)
save_plots(df.oe,'offender-enemy',nfirst)



