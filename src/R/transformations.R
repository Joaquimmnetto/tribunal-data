library(dplyr)

range01 <- function(x){(x-min(x))/(max(x)-min(x))}


#-----------------Carregamento dos dados e pré-processamento-----------------------------

#knitr::opts_chunk$set(dev = 'png')
players <- read.csv("data/csv/players.csv", header = FALSE)
matches <- read.csv("data/csv/matches.csv", header = FALSE)

#players <- read.csv("data/csv/players_033.csv", header = FALSE)
#matches <- read.csv("data/csv/matches_033.csv", header = FALSE)

names(matches) <- c("case", "match", "premade", "most.common.offense",
                   "reports.allies", "reports.enemies", "reports.case", "time.played")

names(players) <- c("case", "match", "relation.offender", "champion", "kills", "deaths",
                    "assists", "gold", "outcome")

players$champion <- as.factor(players$champion)

players <- players %>% mutate(id = seq.int(nrow(players)))

matches$premade = NULL
matches$reports.case = NULL


players <- players[players$relation.offender != "",]
players$relation.offender <- factor(players$relation.offender)

matches <- matches[matches$most.common.offense != "",]
matches$most.common.offense <- factor(matches$most.common.offense)

#matches$premade <- factor(matches$premade)
#levels(matches$premade) <- c("No", "Yes")

#--------------------Cálculo da peformance-----------------------------------

players <- players %>% mutate(kda = (kills + assists)/(deaths + 1))

#matches.players <- matches %>% left_join(players, by = c("case", "match"))

#grouping gold and kda by case and match, and assigning the info to the matches frame.
matches <- matches %>% left_join(aggregate(gold ~ case+match, data=players,FUN=sum), by=c('case','match') )
matches <- plyr::rename(matches,c("gold"="match.gold"))

matches <- matches %>% left_join( aggregate(kda ~ case+match, data=players,FUN=sum), by=c('case','match') )
matches <- plyr::rename(matches,c("kda"="match.kda"))


perf <- players[c("id","case","match","gold","kda")] %>% 
                  left_join( matches[ c("case","match","match.gold","match.kda") ],by=c("case","match") ) %>%
                  mutate(perc.gold = (gold/match.gold)) %>%
                  mutate(perc.kda = (kda/match.kda))

players <- players %>% left_join(perf[c("id","perc.gold","perc.kda")],by=c("id"))
rm(perf)

#Final metric
players <- players %>% mutate( performance = sqrt(perc.gold^2+perc.kda^2)/sqrt(2) ) 


#--------------Calculo da contaminação-------------------------------------------------

alpha = 1.5

reason.by.team <- unique(matches[, 1:8]) %>%
  select(most.common.offense, reports.allies, reports.enemies) %>%
  mutate(pnd.total.reports = reports.allies + alpha*reports.enemies)

reports.by.reason <- aggregate(pnd.total.reports ~ most.common.offense, data = reason.by.team, FUN = sum) %>% 
                     mutate(frequency = as.vector(table(matches$most.common.offense))) %>%
                     mutate(report.ratio = total.reports.pnd/frequency)


#passing the ratio created above to the matches table, so that we have the ratios for each match.
for(i in 1:nrow(matches)) { 
  matches[i, "report.ratio"] <- reports.by.reason[matches[i, "most.common.offense"] == reports.by.reason$most.common.offense, 5]
}
rm(i)
  
matches.players <- matches.players %>% left_join( matches %>% select(case,match,report.ratio), by=c("case","match"))

matches <- matches %>% mutate( match.contamination = report.ratio * (reports.allies/4 + reports.enemies/5) )


matches.tox <- data.frame(matches$case,matches$match,matches$match.contamination)
names(matches.tox) <- c('case','match','match.contamination')

matches.players <- matches.players %>% left_join(matches.tox,by=c('case','match'))
matches.players <- matches.players %>% mutate( team.contamination = ifelse(relation.offender=='enemy', report.ratio*reports.enemies/5, report.ratio*reports.allies/4) )

rm(matches.tox)


#Ideas for the future: Work with a concept of 'match toxicity', using the reports to measure, and then try to split that on each player.
#Ou FODASSE essa história e repensar os objetivos.
#TODO: arquivo para plotar os gráficos.

########################################################################
