require(dplyr)
require(data.table)

#--------------------Cálculo da peformance-----------------------------------

#Processing KDA
players <- players[,kda := (kills + assists)/(deaths + 1)]

#grouping gold and kda by case and match, and assigning the info to the matches frame.
matches <- matches[ players[, .(match.gold = sum(gold)), by = .(case, match)] ]
matches <- matches[ players[, .(match.kda = sum(kda)), by = .(case, match)] ]

players <- players[,id := seq.int(nrow(players))]
#Aux table for performance processing
perf <- players[, .(id, case, match, gold, kda)][matches[,.(case, match, match.gold, match.kda)],on=.(case,match) ]
perf <- perf[, perc.gold := (gold/match.gold)]
perf <- perf[, perc.kda := ifelse(match.kda > 0, kda/match.kda, 0)]
players <- players[perf[,.(id,perc.gold,perc.kda)], on ="id"]
rm(perf)

#Player performance
players <- players[, performance := (perc.gold+perc.kda)/2]

#Team peformance
team.performance <- players[, .(performance = sum(performance)), by=.(case,match,relation.offender)]

allies.performance <- team.performance[relation.offender == 'ally'][,ally.performance := performance/4][,c('relation.offender','performance') := NULL] 
enemies.performance <- team.performance[relation.offender == 'enemy'][,enemy.performance := performance/5][,c('relation.offender','performance') := NULL] 
offender.performance <- team.performance[relation.offender == 'offender'][,offender.performance := performance][,c('relation.offender','performance') := NULL] 


matches <- matches[allies.performance][enemies.performance][offender.performance]
                          
rm(team.performance)
rm(allies.performance)
rm(enemies.performance)
rm(offender.performance)
