require(data.table)
require(wordcloud)
require(tm)
require(dplyr)

df.ae <- setDT(fread("data/df_ae.csv",header=FALSE,showProgress=TRUE))
df.ao <- setDT(fread("data/df_ao.csv",header=FALSE,showProgress=TRUE))
df.eo <- setDT(fread("data/df_eo.csv",header=FALSE,showProgress=TRUE))

rows <- c("word","count")
setnames(df.ae, names(df.ae),rows)
setnames(df.ao, names(df.ao),rows)
setnames(df.eo, names(df.eo),rows)


stwords <- stopwords("english")
df.ae <- df.ae[!(word %in% stwords)]
df.ao <- df.ao[!(word %in% stwords)]
df.eo <- df.eo[!(word %in% stwords)]
 
wordcloud(df.ae$word, df.ae$count, max.words=200, random.order=FALSE)
dev.print(png, 'wc.df.ae.smpl.png',width=500,height=500)
 
wordcloud(df.ao$word, df.ao$count, max.words=200, random.order=FALSE)
dev.print(png, 'wc.df.ao.smpl.png',width=500,height=500)
 
wordcloud(df.eo$word, df.eo$count, max.words=200, random.order=FALSE)
dev.print(png, 'wc.df.eo.smpl.png',width=500,height=500)
 
 
df.ea <- df.ae %>% mutate(count = -1*count)
wordcloud(df.ea$word, df.ea$count, max.words=200, random.order=FALSE)
dev.print(png, 'wc.df.ea.smpl.png',width=500,height=500)

df.oa <- df.ao %>% mutate(count = -1*count)
wordcloud(df.oa$word, df.oa$count, max.words=200, random.order=FALSE)
dev.print(png, 'wc.df.oa.smpl.png',width=500,height=500)

df.oe <- df.eo %>% mutate(count = -1*count)
wordcloud(df.oe$word, df.oe$count, max.words=200, random.order=FALSE)
dev.print(png, 'wc.df.oe.smpl.png',width=500,height=500)



