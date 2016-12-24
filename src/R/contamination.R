require(dplyr)

#--------------Calculo da contaminação-------------------------------------------------

alpha = 1.5
nallies = 4
nenemies = 5

matches <- matches[, report.ratio := sum(reports.allies + alpha*reports.enemies)/.N, by = most.common.offense]
matches <- matches[, report.ratio := report.ratio/max(report.ratio)]

#calculo das contaminações
matches <- matches[, ally.contamination := report.ratio*reports.allies/4]
matches <- matches[, enemy.contamination := report.ratio*reports.enemies/5]
matches <- matches[, match.contamination := (ally.contamination+enemy.contamination)/2]
matches <- matches[, report.ratio := NULL]

