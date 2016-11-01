#matchs was a mistake.
#matches.players <- matchs.players
#rm(matchs.players)

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


#Now, after all the failures to make a toxic behavior metric based on player performance,
#we try to make a metric for toxic behavior for each match, based on report data.

#removing the noise from most.common.ofense
#matchs <- matchs %>% filter(most.common.offense != "")
reports.by.reason<- reports.by.reason %>% filter(most.common.offense != "")

#Puting the frequency on with each type of report occours on matches
reports.by.reason <- reports.by.reason %>% mutate( frequency = as.vector(table(matchs$most.common.offense))[2:8] )

#Making the ratio of total.reports/frequency.
#With this we have the report ratio for each match where that type of toxic behavior occours.
#We use this to determine which types of toxic behavior are more annoying to the player.
reports.by.reason <- reports.by.reason %>% mutate(ratio = total.reports/frequency)

#passing the ratio created above to the matchs table, so that we have the ratios for each match.
for(i in 1:nrow(matchs)) { 
  matchs[i, "report.gravity"] <- reports.by.reason[matchs[i, "most.common.offense"] == reports.by.reason$most.common.offense, 4]
}
rm(i)

#We propose a formula for the toxicity level on each match based on the reports occoured on that match.
#The formula is based on weights, where we first divide the reports of each team by its number of players, so we get the player/report ratio for the match
#on the ally team we remove the offensor, because he can't report himself, even if he wanted to, due to game UI limitations.

# Then we give a greater weight to the enemy report due the fact that the enemy isn't usualy affected by the toxic behavior, so, on most cases it have
#less motivations to make a report. Then a enemy report must mean that the toxic player allies had to go out of their way 
#to ask the enemy team for reports, or that the toxic behavior was so bad that the enemy team noticed and reported anyway, even if it was beneficial to them.

#finnaly, we recognize that are some kinds of toxic behavior that are more accute than others, and use the report gravity calculated previsiouly as a weight.

enemy.ally.report.ratio <- sum(matchs$reports.allies)/sum(matchs$reports.enemies)
matchs <- matchs %>% mutate( contamination = report.gravity * ((reports.allies/4) + 2*(reports.enemies/5)) )


#then, we normalize it by the highest toxic behavior value possible(highest value of report.gravity, and every player has reported).
#The value is 6.928208

matchs <- matchs %>% mutate( contamination = contamination/max(contamination) )

#Ideas for the future: Work with a concept of 'match toxicity', using the reports to measure, and then try to split that on each player.
#Ou FODASSE essa história e repensar os objetivos.
#TODO: arquivo para plotar os gráficos.








