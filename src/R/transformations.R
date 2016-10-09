players <- read.csv("data/csv/players.csv", header = FALSE)
matches <- read.csv("data/csv/matches.csv", header = FALSE)

names(matches) <- c("case", "match", "premade", "most.common.offense",
                   "reports.allies", "reports.enemies", "reports.case", "time.played")

names(players) <- c("case", "match", "relation.offender", "champion", "kills", "deaths",
                    "assists", "gold", "outcome")

matches$premade <- factor(matches$premade)
levels(matches$premade) <- c("No", "Yes")

players <- players %>% mutate(KDA = (kills + assists)/(deaths + 1))

matches.players <- matches %>% left_join(players, by = c("case", "match"))

allies <- matches.players %>% filter(relation.offender == "ally")
enemies <- matches.players %>% filter(relation.offender == "enemy")
offenders <- matches.players %>% filter(relation.offender == "offender")

reason.by.team <- unique(matches.players[, 1:8]) %>%
    select(most.common.offense, reports.allies, reports.enemies) %>%
    mutate(total.reports = reports.allies + reports.enemies)

reports.by.reason <- aggregate(total.reports ~ most.common.offense, 
                               data = reason.by.team, FUN = sum)

case.match <- unique(matches.players %>%
                         select(case, match, relation.offender, outcome))

allies.win <- allies %>% filter(outcome == "Win")
enemies.win <- enemies %>% filter(outcome == "Win")
offenders.win <- offenders %>% filter(outcome == "Win")
