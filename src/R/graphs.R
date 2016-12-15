require(ggplot2)
require(dplyr)

save_graph <- function(plot){
  ggsave(paste(deparse(substitute(plot)),'.png',sep=''), plot=plot, device='png')
}

#coluna match.winner:mostra qual o time que venceu a partida(ally,enemy)
matches <- matches %>% 
  left_join(
    players %>%
      select(case,match,relation.offender,outcome) %>%
      filter(outcome=='Win' & relation.offender!='offender') %>%
      unique() %>%
      rename(match.winner = relation.offender) %>%
      select(case,match,match.winner)
  )

#--------------Métrica de desempenho--------------------

#perc.outcome.point <- ggplot(data=players,aes(x=perc.gold,y=perc.kda,color=outcome))+geom_point()
#save_graph(perc.outcome.point)
#rm(perc.outcome.point)

#boxplot de performance X outcome. Mostra que a métrica cobre bem os jogadores vencedores.
perf.outcome.box <- ggplot(data=players) + geom_boxplot(aes(x=outcome,y=performance))
save_graph(perf.outcome.box)
rm(perf.outcome.box)

#boxplot de performance x relattion.offender. Mostra que o time aliado tem um desempenho levemente pior do que o inimigo.
perf.offender.box <- ggplot(data = players) + geom_boxplot(aes(x=relation.offender,y=performance))
save_graph(perf.offender.box)
rm(perf.offender.box)

#boxplot de performance x relation x outcome. Reforça a métrica, e mostra que a diferença de performance 
#entre times vencedores de diferentes realation.offender é minima.
perf.offender.outcome.box <- ggplot(data=players) + geom_boxplot(aes(x=relation.offender,y=performance))
save_graph(perf.offender.outcome.box)
rm(perf.offender.outcome.box)

#perf.outcome.offender.box <- ggplot(data=players,aes(x=outcome,y=performance,color=relation.offender)) + geom_boxplot()
#save_graph(perf.outcome.offender.box)
#rm(perf.outcome.offender.box)

perf.hist <- ggplot(data=players) + geom_histogram(aes(x=performance),bins=20)

save_graph(perf.hist)
rm(perf.hist)


#--------------Métrica de toxicidade por partida--------------------

#nuvem de pontos bonita, boa pra mostrar a distribuição visualmente
perf.mtox.points <- ggplot(data = matches) + 
  geom_point(aes(x=ally.contamination, y = ally.performance, color=match.winner)) 
  geom_point(aes(x=enemy.contamination, y = enemy.performance, color=match.winner))

save_graph(perf.mtox.points)
rm(perf.mtox.points)

#Distribuição da contaminação. Não é bonitinha mas é tecnica.
mtox.hist <- ggplot(data=matches,aes(x=match.contamination)) + geom_histogram(bins=10)

save_graph(mtox.hist)
rm(mtox.hist)

#Mostra como o desempenho no geral cai com a contaminação
#perf.mtox.lm <- ggplot(data = mtpl.view) + geom_smooth(aes(x=match.contamination,y=performance),method=lm)

#Mostra como ally e offender caem com a contaminação, enquando o enemy sobe
#Remover outliers para plotar isso.
matches.no.out <- matches
threshold <- min(boxplot(matches.no.out[,c("ally.contamination")])$out)
matches.no.out <- matches.no.out %>% filter(ally.contamination <= threshold)

threshold <- min(boxplot(matches.no.out[,c("ally.performance")])$out)
matches.no.out <- matches.no.out %>% filter(ally.performance <= threshold)

threshold <- min(boxplot(matches.no.out[,c("enemy.contamination")])$out)
matches.no.out <- matches.no.out %>% filter(enemy.contamination <= threshold)

threshold <- min(boxplot(matches.no.out[,c("enemy.performance")])$out)
matches.no.out <- matches.no.out %>% filter(enemy.performance <= threshold)

threshold <- min(boxplot(matches.no.out %>% select(offender.performance))$out)
matches.no.out <- matches.no.out %>% filter(offender.performance <= threshold)

noout.perf.mtox.offender.lm <- ggplot(data = matches.no.out) + 
  geom_smooth(aes(x=ally.contamination,y=ally.performance), method="lm", color='blue') + 
  geom_smooth(aes(x=enemy.contamination,y=enemy.performance), method="lm", color='red') + 
  geom_smooth(aes(x=ally.contamination,y=offender.performance), method="lm", color='purple')+
  labs(x="contamination",y="performance")

save_graph(noout.perf.mtox.offender.lm)
rm(noout.perf.mtox.offender.lm)



perf.mtox.offender.lm <- ggplot(data = matches) + geom_smooth(aes(x=ally.contamination,y=ally.performance), method="lm", color='blue') + 
  geom_smooth(aes(x=enemy.contamination,y=enemy.performance), method="lm", color='red') + 
  geom_smooth(aes(x=ally.contamination,y=offender.performance), method="lm", color='purple')+
  labs(x="contamination",y="performance")

save_graph(perf.mtox.offender.lm)
rm(perf.mtox.offender.lm)


#---------------Comparações com tipos de ofensa--------------------------------

#
mtox.offense.hist <- ggplot(matches) + 
  geom_histogram(aes(x=match.contamination, fill=most.common.offense), bins=15, position='fill')

save_graph(mtox.offense.hist)
rm(mtox.offense.hist)

#
mtox.offense.hist.enemy <- ggplot(matches) + 
  geom_histogram(aes(x=enemy.contamination, fill=most.common.offense),bins=15,position='fill')

save_graph(mtox.offense.hist.enemy)
rm(mtox.offense.hist.enemy)

#
mtox.offense.hist.ally <- ggplot(matches) + 
  geom_histogram(aes(x=ally.contamination, fill=most.common.offense), bins=15, position='fill')

save_graph(mtox.offense.hist.ally)
rm(mtox.offense.hist.ally)

#
#perf.offense.hist <- ggplot(matches) + 
#                                   geom_histogram(aes(x=match.performance, fill=most.common.offense),bins=15,position='fill') + 
#                                   scale_x_reverse()
#save_graph(perf.offense.hist)
#rm(perf.offense.hist)

#
perf.offense.hist.enemy <- ggplot(matches) + 
  geom_histogram(aes(x=enemy.performance, fill=most.common.offense), bins=15, position='fill') + 
  scale_x_reverse()

save_graph(perf.offense.hist.enemy)
rm(perf.offense.hist.enemy)

#
perf.offense.hist.ally <- ggplot(matches) + 
  geom_histogram(aes(x=ally.performance, fill=most.common.offense), bins=15,position='fill') + 
  scale_x_reverse()

save_graph(perf.offense.hist.ally)
rm(perf.offense.hist.ally)

#mostra que o time aliado sofre muito mais com o comportamento tóxico do que o time inimigo.
#contudo, não é como se o time inimigo fosse completamente 'limpo'
ttox.ofense.box <- ggplot(matches) + 
  geom_boxplot(aes(x='enemy',y=enemy.contamination)) +
  geom_boxplot(aes(x='ally',y=ally.contamination)) +
  labs(x='team',y='contamination')

save_graph(ttox.ofense.box)
rm(ttox.ofense.box)