#grouping gold by case and match, and assigning the info to a new frame.
aggr.perf.sum <- aggregate(gold ~ case+match, data=matches.players,FUN=sum)

#renaming gold column to avoid column name conflict issues on near future.
aggr.perf.sum <- plyr::rename(aggr.perf.sum,c("gold"="match.gold"))

#grouping by kda and assigning to a new column on aggr.perf.sum
aggr.perf.sum <- aggr.perf.sum %>% mutate(match.kda = aggregate(kda~case+match,data=matches.players,FUN=sum)$kda)

#storing match.gold and match.kda on matches for better organization
matchs <- matchs %>% left_join(aggr.perf.sum,by=c("case","match"))

#joining match.gold and match.kda on The Big Frame.
matches.players <- matches.players %>% left_join(aggr.perf.sum,by=c("case","match"))

#removing because it's useless now
rm(aggr.perf.sum)


#percentage gold and kda metrics
matches.players <- matches.players %>% mutate(perc.gold = (gold/match.gold) )
matches.players <- matches.players %>% mutate(perc.kda = (kda/match.kda) )

#finnaly, performance metric. Its the euclidean distance from origin to (perc.gold,perc.kda).
#normalized by sqrt(2) because its the highest performance achievable(player amassed 100%(1) kda and 100%(1) gold)
#hence, its the (1,1) point and its performance its sqrt(2).
matches.players <- matches.players %>% mutate( performance = sqrt(perc.gold^2+perc.kda^2)/sqrt(2) ) 
#further proof for the metric on \img folder.

#Reproducing one of the failed metrics here. The assumption is still that the toxicity has a negative influence on peformance(and I think it have) 
#see /img folder boxplot_perf_outcome_offender.png, win column.
#its a veeeery small difference, so Kazuki plz use some statistical magic to see if its meaningful or not.

#Anyway, the idea is to compare the players to the average performance of enemy team on its best(the winning matches). 
#It didnt worked. Make some boxplots and its evident.
mean.enemy.perf <- mean( (matches.players %>% filter(relation.offender=='enemy') %>% filter(outcome=='Win'))$performance )
matches.players <- matches.players %>% mutate(toxicity.fail = mean.enemy.perf - performance)

#Ideas for the future: Work with a concept of 'match toxicity', using the reports to measure, and then try to split that on each player.

#Ou FODASSE essa história e repensar os objetivos.
#TODO: arquivo para plotar os gráficos.








