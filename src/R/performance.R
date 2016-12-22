require(dplyr)

#--------------------Cálculo da peformance-----------------------------------

#Processing KDA
players <- players[,kda := (kills + assists)/(deaths + 1)]

#grouping gold and kda by case and match, and assigning the info to the matches frame.
matches <- matches[ players[,.(match.gold = sum(gold)),by=.(case,match)] ]

matches <- matches[ players[,.(match.kda = sum(kda)),by=.(case,match)]]
#matches <- matches %>% left_join( aggregate(kda ~ case+match, data=players,FUN=sum), by=c('case','match') )
#matches <- plyr::rename(matches,c("kda"="match.kda"))


#Aux table for performance processing
perf <- players[c("id","case","match","gold","kda")] %>% 
  left_join( matches[ c("case","match","match.gold","match.kda") ],by=c("case","match") ) %>%
  mutate(perc.gold = (gold/match.gold)) %>%
  mutate(perc.kda = ifelse(match.kda>0,kda/match.kda,0) )
  

players <- players %>% left_join(perf[c("id","perc.gold","perc.kda")],by=c("id"))
rm(perf)

#Player performance
players <- players %>% mutate( performance = sqrt(perc.gold^2+perc.kda^2)/sqrt(2))
players <- players %>% mutate( performance2 = (perc.gold+perc.kda)/2 )
players <- players %>% mutate( performance3 = (perc.gold)) 
players <- players %>% mutate( performance4 = (perc.kda))

#Team peformance
team.performance <- players %>% 
                    group_by(case,match,relation.offender) %>% 
                    summarize(performance=sum(performance), performance2=sum(performance2), 
                                performance3=sum(performance3), performance4=sum(performance4))


allies.performance <- team.performance %>%  
                       filter(relation.offender == 'ally') %>% 
                      select(case, match, performance, performance2, performance3, performance4) %>%
                      mutate(performance = performance/4, performance2 = performance2/4,performance3 = performance3/4,performance4 = performance4/4) %>% 
                      rename(ally.performance = performance, ally.performance2 = performance2, ally.performance3 = performance3, ally.performance4 = performance4) 

enemies.performance <- team.performance %>%  
                      filter(relation.offender == 'enemy') %>%
                      select(case, match, performance, performance2, performance3, performance4) %>%
                      mutate(performance = performance/5, performance2 = performance2/5,performance3 = performance3/5,performance4 = performance4/5) %>% 
                      rename(enemy.performance = performance, enemy.performance2 = performance2, enemy.performance3 = performance3, enemy.performance4 = performance4) 

offender.performance <- team.performance %>%  
                      filter(relation.offender == 'offender') %>%
                    select(case, match, performance, performance2, performance3, performance4) %>%
                    rename(offender.performance = performance, offender.performance2 = performance2, offender.performance3 = performance3, offender.performance4 = performance4) 


matches <- matches %>% left_join(allies.performance) %>% 
                          left_join(enemies.performance) %>% 
                          left_join(offender.performance)
                          #mutate(match.performance = (4*ally.performance)+(5*enemy.performance)+offender.performance)
              

rm(team.performance)
rm(allies.performance)
rm(enemies.performance)
rm(offender.performance)
