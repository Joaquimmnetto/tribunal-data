require(tm)
require(wordcloud)
require(SnowballC)
require(data.table)
require(dtplyr)

#matches.in <- matches[matches$most.common.offense=="Helping enemy",]
#matches.in <- matches[matches$most.common.offense=="Verbal offense",]
#matches.in <- matches[matches$most.common.offense=="Negative Attitude",]
#matches.in <- matches[matches$most.common.offense=="Others",]


ally.text <- Corpus(VectorSource(matches.in$report.text.allies)) %>% 
              tm_map(PlainTextDocument) %>% 
              tm_map(removePunctuation) %>% 
              tm_map(removeWords,stopwords('english'))
enemy.text <- Corpus(VectorSource(matches.in$report.text.enemies)) %>% 
                tm_map(PlainTextDocument) %>% 
                tm_map(removePunctuation) %>% 
                tm_map(removeWords,stopwords('english'))


wordcloud(ally.text,max.words=100,random.order=FALSE)
wordcloud(enemy.text,max.words=100,random.order=FALSE)
