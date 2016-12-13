require(dplyr)

#--------------------Cálculo da peformance-----------------------------------

#Processing KDA
players <- players %>% mutate(kda = (kills + assists)/(deaths + 1))

#grouping gold and kda by case and match, and assigning the info to the matches frame.
matches <- matches %>% left_join(aggregate(gold ~ case+match, data=players,FUN=sum), by=c('case','match') )
matches <- plyr::rename(matches,c("gold"="match.gold"))

matches <- matches %>% left_join( aggregate(kda ~ case+match, data=players,FUN=sum), by=c('case','match') )
matches <- plyr::rename(matches,c("kda"="match.kda"))


#Aux table for performance processing
perf <- players[c("id","case","match","gold","kda")] %>% 
  left_join( matches[ c("case","match","match.gold","match.kda") ],by=c("case","match") ) %>%
  mutate(perc.gold = (gold/match.gold)) %>%
  mutate(perc.kda = ifelse(match.kda>0,kda/match.kda,0) )
  

players <- players %>% left_join(perf[c("id","perc.gold","perc.kda")],by=c("id"))
rm(perf)

#Player performance
players <- players %>% mutate( performance = sqrt(perc.gold^2+perc.kda^2)/sqrt(2) )

#Team peformance
team.performance <- aggregate(performance ~ case+match+relation.offender, data=players, FUN=sum )
team.performance <- aggregate(performance ~ case+match+relation.offender, data=players, FUN=sum )


allies.performance <- team.performance %>%  
                       filter(relation.offender == 'ally') %>% 
                       select(case, match, performance) %>%
                       mutate(performance = performance/4) %>% 
                       rename(ally.performance = performance) 

enemies.performance <- team.performance %>%  
                      filter(relation.offender == 'enemy') %>%
                      select(case, match, performance) %>%
                      mutate(performance = performance/5) %>% 
                      rename(enemy.performance = performance) 


offender.performance <- team.performance[team.performance$relation.offender == 'offender',c("case","match","performance")] %>% 
                          rename(offender.performance = performance)

matches <- matches %>% left_join(allies.performance,by=c('case','match')) %>% 
                          left_join(enemies.performance,by=c('case','match')) %>% 
                          left_join(offender.performance,by=c('case','match'))
              

rm(team.performance)
rm(allies.performance)
rm(enemies.performance)
rm(offender.performance)
