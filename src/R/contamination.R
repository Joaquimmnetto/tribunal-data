require(dplyr)

#--------------Calculo da contaminação-------------------------------------------------

alpha = 1.5
nallies = 4
nenemies = 5

reports.by.reason <- 
  aggregate(pnd.total.reports ~ most.common.offense, 
            data = matches %>% mutate(pnd.total.reports = reports.allies + alpha*reports.enemies), FUN = sum) %>% 
  mutate(frequency = as.vector(table(matches$most.common.offense))) %>%
  mutate(report.ratio = pnd.total.reports/frequency)


f <- function(match_mco){
  return((reports.by.reason %>% filter(most.common.offense == match_mco))$report.ratio)
}
matches <- matches %>% rowwise() %>% mutate(report.ratio = f(most.common.offense) )
rm(f)

#calculo das contaminações
matches <- matches %>% mutate(ally.contamination = report.ratio*reports.allies/4)
matches <- matches %>% mutate(enemy.contamination = report.ratio*reports.enemies/5)
matches <- matches %>% mutate(match.contamination = ally.contamination+enemy.contamination)

matches$report.ratio <- NULL
