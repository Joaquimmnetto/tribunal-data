setwd("~/PyCharm-Workspace/tribunaldb/data/full/")
chat_fl <- 'chat_targets.csv'

chat_targets <- setDT(fread(chat_fl, header = FALSE, sep=',', showProgress=TRUE, 
														colClasses = c("factor","factor","factor","factor")))
setnames(chat_targets, names(chat_targets), c("case", "match",'relation.offender','target'))

chat_targets <- data.table(table(chat_targets))

chat_targets$case <- as.factor(chat_targets$case)
chat_targets$match <- as.factor(chat_targets$match)
chat_targets$relation.offender <- as.factor(chat_targets$relation.offender)
chat_targets$target <- as.factor(chat_targets$target)

setkey(chat_targets, case, match, relation.offender, target)
setkey(groups, case, match, relation.offender)
setkey(matches, case, match)

chat_targets <- chat_targets[relation.offender!=''][target!='Unassigned']

all_targets <- chat_targets[target=='All', .(case, match, relation.offender, N)]
team_targets <- chat_targets[target=='Team1', .(case, match, relation.offender, N)]
team2_targets <- chat_targets[target=='Team2', .(case, match, relation.offender, N)]

team_targets <- team_targets[, .(case, match, relation.offender, N = team_targets$N + team2_targets$N)]
rm(team2_targets)

groups <- merge(groups, all_targets[,.(case, match, relation.offender, num.all = N)], all.x=TRUE)
groups <- merge(groups, team_targets[,.(case, match, relation.offender, num.team = N)], all.x=TRUE)

rm(team_targets)
rm(all_targets)

matches <- matches[groups[relation.offender=='offender', .(case,match, offender.all = 60*(num.all))]]
matches <- matches[, offender.all := offender.all/time.played]
matches <- matches[groups[relation.offender=='offender', .(case,match, offender.team = 60*(num.team))]]
matches <- matches[, offender.team := offender.team/time.played]

#med.t.test(matches[offender.all == 0]$enemy.contamination, matches[offender.all > 0]$enemy.contamination)
#med.t.test(matches[offender.all == 0]$ally.contamination, matches[offender.all > 0]$ally.contamination)


