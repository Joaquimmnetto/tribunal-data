players <- read.csv("data/csv/players.csv", header = FALSE)
matchs <- read.csv("data/csv/matchs.csv", header = FALSE)

names(matchs) <- c("case", "match", "premade", "most.common.offense",
                   "reports.allies", "reports.enemies", "reports.case", "time.played")

names(players) <- c("case", "match", "relation.offender", "champion", "kills", "deaths",
                    "assists", "gold", "outcome")

matchs.players <- matchs %>% left_join(players, by = c("case", "match"))
matchs.players <- matchs.players %>% mutate(kda = (kills + assists)/(deaths + 1))

allies <- matchs.players %>% filter(relation.offender == "ally")
enemies <- matchs.players %>% filter(relation.offender == "enemy")
offenders <- matchs.players %>% filter(relation.offender == "offender")

reason.by.team <- unique(matchs.players[, 1:8]) %>%
    select(most.common.offense, reports.allies, reports.enemies) %>%
    mutate(total.reports = reports.allies + reports.enemies)

reports.by.reason <- aggregate(total.reports ~ most.common.offense, 
                               data = reason.by.team, FUN = sum)

case.match <- unique(matchs.players %>%
                         select(case, match, relation.offender, outcome))

allies.win <- allies %>% filter(outcome == "Win")
enemies.win <- enemies %>% filter(outcome == "Win")
offenders.win <- offenders %>% filter(outcome == "Win")
