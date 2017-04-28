require(dplyr)

#--------------Calculo da contaminação-------------------------------------------------

alpha = 1.5
nallies = 4
nenemies = 5

#matches <- matches[, report.ratio := sum(reports.allies + alpha*reports.enemies)/.N, by = most.common.offense]
#matches <- matches[, report.ratio := report.ratio/max(report.ratio)]

#calculo das contaminações
matches <- matches[, ally.contamination := reports.allies/4]
matches <- matches[, enemy.contamination := reports.enemies/5]
matches <- matches[, match.contamination := (ally.contamination+enemy.contamination)/2]
matches <- matches[, report.ratio := NULL]

mean.cont.offense <- matches[,.(mean.match.cont = mean(match.contamination),median.match.cont = median(match.contamination)), by=most.common.offense]


#A presença de uma justificativa textual na denúncia está associada com um grau maior de toxicidade?
# "allies-wout"
# summary(matches[report.text.allies=='']$ally.contamination)
# "allies-with"
# summary(matches[report.text.allies!='']$ally.contamination)
# "allies-full"
# summary(matches$ally.contamination)
# 
# "enemies-wout"
# summary(matches[report.text.enemies=='']$enemy.contamination)
# "enemies-with"
# summary(matches[report.text.enemies!='']$enemy.contamination)
# "enemies-full"
# summary(matches$enemy.contamination)
# 
# 'full-wout'
# summary(matches[report.text.allies=='' & report.text.enemies=='']$match.contamination)
# 'full-with'
# summary(matches[report.text.allies!='' | report.text.enemies!='']$match.contamination)
# 'full-full'
# summary(matches$match.contamination)
# 
# nrow(matches[report.text.allies==''&report.text.enemies==''])/nrow(matches)
# 
# p <- ggplot() + geom_boxplot(data=matches,aes(x="ally-full",y=ally.contamination)) + 
#         geom_boxplot(data=matches[report.text.allies==''],aes(x="ally-wout",y=ally.contamination)) +
#         geom_boxplot(data=matches[report.text.allies!=''],aes(x="ally-with",y=ally.contamination)) +
#         geom_boxplot(data=matches,aes(x="enemy-full",y=enemy.contamination)) + 
#         geom_boxplot(data=matches[report.text.enemies==''],aes(x="enemy-wout",y=enemy.contamination)) +
#         geom_boxplot(data=matches[report.text.enemies!=''],aes(x="enemy-with",y=enemy.contamination))
# 
# nrow(matches[report.text.allies!=''])/nrow(matches)
