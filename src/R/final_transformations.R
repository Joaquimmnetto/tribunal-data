range01 <- function(x){(x-min(x))/(max(x)-min(x))}
#t-test comparando a métrica de performance nova e a antiga. Pelo o que eu sei interpretar de t-test ele tá dizendo que a diferença é significativa
#Contudo,a métrica nova mostra resultados semelhantes a antiga, e não quebra quando combinada com valores da partida.
t.test(scale(matches.players$performance.new),range01(matches.players$performance.old))


#Não há correlação entre a performance na partida e a contaminação(oh no)
#Isso não faz sentido na comparação com os gráficos, pode ser só eu lendo info. estatistica de maneira errada mesmo.
cor(matches.players$match.contamination,matches.players$performance.old)

matches.players <- matches.players %>% mutate( team.contamination = ifelse(relation.offender=='enemy', report.ratio*reports.enemies/5, report.ratio*reports.allies/4) )

ally.team <- matches.players[matches.players$relation.offender!='enemy',]
enemy.team <- matches.players[matches.players$relation.offender=='enemy',]
#summary para time aliado
summary(ally.team$team.contamination)
#summary para time inimigo
summary(enemy.team$team.contamination)

t.test(ally.team$team.contamination,enemy.team$team.contamination)