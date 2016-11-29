library(ggplot2)

case.match <- unique(matches.players %>%
                       select(case, match, relation.offender, outcome))

allies <- matches.players %>% filter(relation.offender == "ally")
enemies <- matches.players %>% filter(relation.offender == "enemy")
offenders <- matches.players %>% filter(relation.offender == "offender")

allies.win <- allies %>% filter(outcome == "Win")
enemies.win <- enemies %>% filter(outcome == "Win")
offenders.win <- offenders %>% filter(outcome == "Win")



common.offense.barplot <- ggplot(data = matches, aes(x = most.common.offense)) +
    geom_bar() +
    xlab("Tipos de ofensas") + ylab("Número de partidas") +
    annotate("text", x = 1, y = 3200, label = "1 partida sem ofensa",
             angle = 90, color = "red") +
    theme(axis.text.x=element_text(angle = 45, hjust = 1))

reports.by.reason.barplot <- ggplot(data = reports.by.reason) +
    geom_bar(aes(x = most.common.offense, y = total.reports),
             stat = "identity") +
    xlab("Tipos de ofensas") + ylab("Número de denúncias") +
    annotate("text", x = 1, y = 5400, label = "nenhuma denúncia",
             angle = 90, color = "red") +
    theme(axis.text.x=element_text(angle = 45, hjust = 1))

time.played.hist <- ggplot(data = matches, aes(x = time.played)) +
    geom_histogram(bins = 100) +
    xlab("Duração da partida (segundos)") + ylab("Número de partidas") +
    annotate("text", x = 1800, y = 2400, color = "red",
             label = "Tempo mínimo de permanência (20 min)") + 
    geom_line(arrow = arrow(ends = "first", type = "closed"),
              data = data.frame(x = c(2000, 1400), y = c(2250, 1900)),
              aes(x = x, y = y), color = "red")

outcome.relation.barplot <- ggplot(data = players) +
    geom_bar(aes(x = relation.offender, fill = outcome)) +
    xlab("Associação com ofensor") + ylab("Número de partidas")

allies.win.time.played.hist <- ggplot(data = allies.win) +
                               geom_histogram(aes(x = time.played), bins = 100) +
                               geom_vline(xintercept = mean(allies.win$time.played), color = "red") +
                               xlim(0, 5000) + 
                               xlab("Duração da partida (segundos)") +
                               ylab("Número de partidas") +
                               ggtitle("Vitória dos aliados") +
                               annotate("text", x = 3000, y = 1700,
                                        color = "red", label = "Média = 2075.5 segundos")

enemies.win.time.played.hist <- ggplot(data = enemies.win) +
                                geom_histogram(aes(x = time.played), bins = 100) +
                                geom_vline(xintercept = mean(enemies.win$time.played), color = "red") +
                                xlim(0, 5000) +
                                xlab("Duração da partida (segundos)") +
                                ylab("Número de partidas") +
                                ggtitle("Vitória dos adversários") +
                                        annotate("text", x = 2900, y = 7800,
                                        color = "red", label = "Média = 1938.2 segundos")

allies.gold.hist <- ggplot(data = allies) +
                    geom_histogram(aes(x = gold), bins = 100) +
                    geom_vline(xintercept = mean(allies$gold), color = "red") +
                    xlim(0, 20500) +
                    xlab("Recompensa (ouro)") +
                    ylab("Número de partidas") +
                    ggtitle("Recompensa dos aliados") +
                    annotate("text", x = 12500, y = 3100, color = "red",
                             label = "Média = 8927.2 (ouro)")

enemies.gold.hist <- ggplot(data = enemies) +
                         geom_histogram(aes(x = gold), bins = 100) +
                         geom_vline(xintercept = mean(enemies$gold), color = "red") +
                         xlim(0, 20500) +
                         xlab("Recompensa (ouro)") +
                         ylab("Número de partidas") +
                         ggtitle("Recompensa dos adversários") +
                         annotate("text", x = 13700, y = 3780, color = "red",
                                  label = "Média = 10166 (ouro)")
rm(allies.win)
rm(enemies.win)
rm(offenders.win)

rm(allies)
rm(enemies)
rm(offenders)

rm(case.match)

mtpl.view <- matches.players

mtpl.view <- mtpl.view[mtpl.view$relation.offender!="",]

#--------------Métrica de desempenho--------------------

perc.outcome.point <- ggplot(data=mtpl.view,aes(x=perc.gold,y=perc.kda,color=outcome))+geom_point() 
#boxplot de performance X outcome. Mostra que a métrica cobre bem os jogadores vencedores.
perf.outcome.box <- ggplot(data=mtpl.view) + geom_boxplot(aes(x=outcome,y=performance))
#boxplot de performance x relattion.offender. Mostra que o time aliado tem um desempenho levemente pior do que o inimigo.
perf.offender.box <- ggplot(data = mtpl.view) + geom_boxplot(aes(x=relation.offender,y=performance.new))
#boxplot de performance x relation x outcome. Reforça a métrica, e mostra que a diferença de performance 
#entre times vencedores de diferentes realation.offender é minima.
perf.offender.outcome.box <- ggplot(data=mtpl.view) + geom_boxplot(aes(x=relation.offender,y=performance.new))

perf.outcome.offender.box <- ggplot(data=mtpl.view,aes(x=outcome,y=performance.new,color=relation.offender)) + geom_boxplot()

perf.hist <- ggplot(data=mtpl.view) + geom_histogram(aes(x=performance.new),bins=20)

ggplot(matches,aes(x = match.toxicity,fill = most.common.offense)) + 
  geom_bar(position = "fill",stat = "identity") + 
  scale_y_continuous(labels = percent_format())

mtpl.view <- mtpl.view[mtpl.view$most.common.offense!="",]
#mtpl.view <- mtpl.view %>% mutate(most.common.offense != "")

#--------------Métrica de toxicidade por partida--------------------

#nuvem de pontos bonita, boa pra mostrar a distribuição visualmente
perf.mtox.outcome.points <- ggplot(data = mtpl.view, aes(x=match.contamination,y=performance.new,color= outcome)) + geom_point()

#Distribuição da contaminação. Não é bonitinha mas é tecnica.
mtox.hist <- ggplot(data=mtpl.view,aes(x=match.contamination)) +geom_histogram(bins=10)

#Mostra como o desempenho no geral cai com a contaminação
perf.mtox.lm <- ggplot(data = mtpl.view) + geom_smooth(aes(x=match.contamination,y=performance.new),method=lm)

#Mostra como ally e offender caem com a contaminação, enquando o enemy sobe
perf.mtox.offender.lm <- ggplot(data = mtpl.view) + geom_smooth(aes(x=match.contamination,y=performance.new,color=relation.offender),method=lm)

report.mtox.spl = ggplot(data=matches,aes(x=match.contamination,y=reports.allies+reports.enemies)) + geom_smooth()

report.mtox.pre.spl = ggplot(data=matches,aes(x=match.contamination,y=reports.allies+reports.enemies,color=premade)) + geom_smooth()

#####

mtox.offense.fx.hist <- ggplot(mtpl.view,aes(x=match.contamination, fill=most.common.offense)) + geom_histogram(bins=10,position='fill')
perf.offense.fx.hist <- ggplot(mtpl.view,aes(x=performance.new, fill=most.common.offense)) + geom_histogram(bins=10,position='fill')

#mostra que o time aliado sofre muito mais com o comportamento tóxico do que o time inimigo.
#contudo, não é como se o time inimigo fosse completamente 'limpo'
ttox.density <- ggplot(mtpl.view) + geom_density(aes(x=team.contamination,color=relation.offender))

#Confirma o comportamento citado acima
ggplot(mtpl.view,aes(x=outcome,y=team.contamination,color=relation.offender)) + geom_boxplot()
