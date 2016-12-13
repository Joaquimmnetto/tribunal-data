require(dplyr)
require(data.table)

players_fl <- "data/csv/players_full.csv"
matches_fl <- "data/csv/matches_full.csv"


#Problemas na construção do csv:
#1. Duplicação de dados
#2. matches e players com partidas disjuntas.

#-----------------Carregamento dos dados e pré-processamento-----------------------------

#Carregando dados...
#Alguns dados estão disjuntos(matches sem players equivalentes e vice-versa) ver issaí. Por enquanto só retirando esses casos do dataset.
players <- fread(players_fl, header = FALSE, sep=',')
matches <- fread(matches_fl, header = FALSE, sep=',')

names(players) <- c("case", "match", "relation.offender", "champion", "kills", "deaths",
                    "assists", "gold", "outcome")
names(matches) <- c("case", "match", "match.type", "most.common.offense","reports.allies", "reports.enemies", "time.played")

#Removendo possíveis duplicatas(Não me pergunte como elas foram parar ai, ver isso depois)
players <- unique(players)
matches <- unique(matches)

#Salvando imagem dos dados sem pre-processamento
#save.image(file = "raw_csv.RData")

#transformando colunas de categoria em factors.
matches$match.type <- factor(matches$match.type)
matches$most.common.offense <- factor(matches$most.common.offense)

#Não é usado por nada!
players$champion = NULL

#Criando colunas auxiliares
#Id é um valor sequencial para dar a cada jogador um identificador único
players <- players %>% mutate(id = seq.int(nrow(players)))
#Casematch é um identificador único para partidas, que nada mais é do que a junção de $case e $match.
players <- players %>% mutate(casematch = paste(case,match))
matches <- matches %>% mutate(casematch = paste(case,match))
#Count é uma coluna auxiliar para contar a quantidade de jogadores em cada partida. A coluna é completamente preenchida por 1s.
players <- players %>% mutate(count = rep.int(1,nrow(players)))

#Remoção de partidas inválidas. Uma partida é inválida se:
  #1. Se uma entrada em matches não tiver seu equivalente em players, e vice-versa.   
  #2. relation.offender ou most.common.offense == ""
  #3. Uma partida não tiver 10 jogadores no seu total.
  


#1
  removal <- setdiff(union(matches$casematch,players$casematch),intersect(matches$casematch,players$casematch))
#2
  removal <- append(removal, players[players$relation.offender == "",c('casematch')])
  removal <- append(removal, matches[matches$most.common.offense == "",c('casematch')])
#3
  removal <- append(removal,(aggregate(count~casematch,data=players,FUN=sum) %>% filter(count < 10))$casematch)
#Removendo possíveis duplicatas.
removal <- unique(removal)


players <- players[!(players$casematch %in% removal),]
matches <- matches[!(matches$casematch %in% removal),]

#Removendo colunas auxiliares que não irão ser mais necessárias.
players$count = NULL
players$casematch = NULL

#Refazendo factors para retirar quaisquer possíveis valores inválidos
players$relation.offender <- factor(players$relation.offender)
matches$most.common.offense <- factor(matches$most.common.offense)
matches$match.type <- factor(matches$match.type)
