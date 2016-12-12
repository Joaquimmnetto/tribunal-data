require(dplyr)

players_fl <- "data/csv/players.csv"
matches_fl <- "data/csv/matches.csv"


#-----------------Carregamento dos dados e pré-processamento-----------------------------

players <- read.csv(players_fl, header = FALSE)
matches <- read.csv(matches_fl, header = FALSE)

names(matches) <- c("case", "match", "premade", "most.common.offense",
                    "reports.allies", "reports.enemies", "reports.case", "time.played")

names(players) <- c("case", "match", "relation.offender", "champion", "kills", "deaths",
                    "assists", "gold", "outcome")


players <- players %>% mutate(id = seq.int(nrow(players)))

matches$premade = NULL
matches$reports.case = NULL
players$champion = NULL

players <- players %>% mutate(casematch = paste(case,match))
players <- players %>% mutate(count = rep.int(1,nrow(players)))
matches <- matches %>% mutate(casematch = paste(case,match))




removal <- append(players[players$relation.offender == "",c('casematch')], 
                  matches[matches$most.common.offense == "",c('casematch')])
removal <- append(removal,(aggregate(count~casematch,data=players,FUN=sum) %>% filter(count < 10))$casematch)
removal <- unique(removal)


players <- players[!(players$casematch %in% removal),]
matches <- matches[!(matches$casematch %in% removal),]

players$count = NULL
players$casematch = NULL


players$relation.offender <- factor(players$relation.offender)
matches$most.common.offense <- factor(matches$most.common.offense)