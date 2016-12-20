require(ggplot2)
require(dplyr)

save_graph <- function(plot){
  ggsave(paste('graphs/graphs_perf_sum/',deparse(substitute(plot)),'.png',sep=''), plot=plot, device='png')
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

matches.no.out <- matches %>% 
  remove.outliers(ally.contamination) %>% 
  remove.outliers(ally.performance) %>% 
  remove.outliers(enemy.contamination) %>% 
  remove.outliers(enemy.performance) %>%
  remove.outliers(offender.performance)




#--------------Métrica de desempenho--------------------
sm.perc.point <- ggplot(players %>% kmn.smoother(1000,x=perc.gold,y=perc.kda)) +
                             geom_point(aes(x=perc.gold,y=perc.kda))
save_graph(sm.perc.outcome.point)
rm(sm.perc.outcome.point)

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
perf.offender.outcome.box <- ggplot(data=players) + geom_boxplot(aes(x=relation.offender,y=performance,color=outcome))
save_graph(perf.offender.outcome.box)
rm(perf.offender.outcome.box)

perf.outcome.offender.box <- ggplot(data=players,aes(x=outcome,y=performance,color=relation.offender)) + geom_boxplot()
save_graph(perf.outcome.offender.box)
rm(perf.outcome.offender.box)

perf.hist <- ggplot(data=players) + geom_histogram(aes(x=performance),bins=20)
save_graph(perf.hist)
rm(perf.hist)

perf.dist <- ggplot(data=players) + geom_density(aes(x=performance))
save_graph(perf.dist)
rm(perf.dist)

perf.team.dist <- ggplot(data=players) + geom_density(aes(x=performance,color=relation.offender))
save_graph(perf.team.dist)
rm(perf.team.dist)



#--------------Métrica de toxicidade por partida--------------------

#nuvem de pontos bonita, boa pra mostrar a distribuição visualmente
perf.mtox.points <- ggplot(data = matches) + 
  geom_point(aes(x=ally.contamination, y = ally.performance, color=match.winner)) 
  geom_point(aes(x=enemy.contamination, y = enemy.performance, color=match.winner))
save_graph(perf.mtox.points)
rm(perf.mtox.points)

sm.perf.mtox.points <- ggplot(matches %>% kmn.smoother(1000,match.contamination,match.performance)) + 
                       geom_point(aes(x=match.contamination,y=match.performance)) + 
                       geom_smooth(aes(x=match.contamination,y=match.performance))
save_graph(sm.perf.mtox.points)
rm(sm.perf.mtox.points)

sm.perf.mtox.team.points <- ggplot() + 
  geom_point(data = matches %>% kmn.smoother(1000,ally.contamination,ally.performance), 
              aes(x=ally.contamination,y=ally.performance), color='blue') + 
  geom_point(data = matches %>% kmn.smoother(1000,enemy.contamination,enemy.performance), 
              aes(x=enemy.contamination,y=enemy.performance), color='red') + 
  geom_point(data = matches %>% kmn.smoother(1000,ally.contamination,offender.performance), 
              aes(x=ally.contamination,y=offender.performance), color='purple')+
  labs(x="contamination",y="performance")
save_graph(sm.perf.mtox.team.points)
rm(sm.perf.mtox.team.points)


#Distribuição da contaminação. Não é bonitinha mas é tecnica.
mtox.hist <- ggplot(data=matches,aes(x=match.contamination)) + geom_histogram(bins=10)
save_graph(mtox.hist)
rm(mtox.hist)

#Mostra como ally e offender caem com a contaminação, enquando o enemy sobe
#Remover outliers para plotar isso.

noout.perf.mtox.offender.lm <- ggplot(data = matches.no.out) + 
  geom_smooth(aes(x=ally.contamination,y=ally.performance), method='lm', color='blue') + 
  geom_smooth(aes(x=enemy.contamination,y=enemy.performance), method='lm', color='red') + 
  geom_smooth(aes(x=ally.contamination,y=offender.performance), method='lm', color='purple')+
  labs(x="contamination",y="performance")

save_graph(noout.perf.mtox.offender.lm)
rm(noout.perf.mtox.offender.lm)

sm.perf.mtox.team.lm <- ggplot() + 
  geom_smooth(data = matches %>% kmn.smoother(1000,ally.contamination,ally.performance), 
             aes(x=ally.contamination,y=ally.performance), method='lm', color='blue') + 
  geom_smooth(data = matches %>% kmn.smoother(1000,enemy.contamination,enemy.performance), 
             aes(x=enemy.contamination,y=enemy.performance), method='lm', color='red') + 
  geom_smooth(data = matches %>% kmn.smoother(1000,ally.contamination,offender.performance), 
             aes(x=ally.contamination,y=offender.performance), method='lm', color='purple')+
  labs(x="contamination",y="performance")
save_graph(sm.perf.mtox.team.lm)
rm(sm.perf.mtox.team.lm)


perf.mtox.offender.lm <- ggplot(data = matches) + 
  geom_smooth(aes(x=ally.contamination,y=ally.performance), method="lm", color='blue') + 
  geom_smooth(aes(x=enemy.contamination,y=enemy.performance), method="lm", color='red') + 
  geom_smooth(aes(x=ally.contamination,y=offender.performance), method="lm", color='purple')+
  labs(x="contamination",y="performance")

save_graph(perf.mtox.offender.lm)
rm(perf.mtox.offender.lm)


#---------------Comparações com tipos de ofensa--------------------------------

#
mtox.offense.hist <- ggplot(matches) + 
  geom_histogram(aes(x=match.contamination, fill=most.common.offense), bins=6, position='fill')

save_graph(mtox.offense.hist)
rm(mtox.offense.hist)

#
mtox.offense.hist.enemy <- ggplot(matches) + 
  geom_histogram(aes(x=enemy.contamination, fill=most.common.offense),bins=6,position='fill')

save_graph(mtox.offense.hist.enemy)
rm(mtox.offense.hist.enemy)

#
mtox.offense.hist.ally <- ggplot(matches) + 
  geom_histogram(aes(x=ally.contamination, fill=most.common.offense), bins=6, position='fill')

save_graph(mtox.offense.hist.ally)
rm(mtox.offense.hist.ally)


perf.offense.hist <- ggplot(matches) + 
                                   geom_histogram(aes(x=match.performance, fill=most.common.offense),bins=15,position='fill') + 
                                   scale_x_reverse()
save_graph(perf.offense.hist)
rm(perf.offense.hist)

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

ttox.ofense.density <- ggplot(matches) + 
  geom_density(aes(x=enemy.contamination),color='red') +
  geom_density(aes(x=ally.contamination),color='blue') +
  labs(x='team',y='contamination')

save_graph(ttox.ofense.density)
rm(ttox.ofense.density)