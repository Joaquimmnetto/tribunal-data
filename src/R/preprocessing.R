require(dplyr)
require(dtplyr)
require(data.table)

players_fl <- "data/full/players.csv"
matches_fl <- "data/full/matches.csv"
#players_fl <- "data/csv/players_sampley.csv"
#matches_fl <- "data/csv/matches_sampley.csv"

#Problemas na construção do csv:
#1. Duplicação de dados
#2. matches e players com partidas disjuntas.

#-----------------Carregamento dos dados e pré-processamento-----------------------------

#Carregando dados...
#Alguns dados estão disjuntos(matches sem players equivalentes e vice-versa) ver issaí. Por enquanto só retirando esses casos do dataset.
players <- setDT(fread(players_fl, header = FALSE, sep=',',showProgress=TRUE))
matches <- setDT(fread(matches_fl, header = FALSE, sep=',',showProgress=TRUE))

setnames(players, names(players),
                c("case", "match", "relation.offender", "champion", "kills", "deaths",
                      "assists", "gold", "outcome"))
 setnames(matches,names(matches),
                 c("case", "match", "match.type", "most.common.offense", 'report.text.allies', 'report.text.enemies',
                     "reports.allies", "reports.enemies", "time.played") )

#atribuindo tipos corretos para as colunas:
#Players
players$case <- as.integer(players$case)
players$match <- as.integer(players$match)
players$relation.offender <- factor(players$relation.offender)
players$champion <- factor(players$champion)
players$kills <- as.integer(players$kills)
players$deaths <- as.integer(players$deaths)
players$assists <- as.integer(players$assists)
players$gold <- as.integer(players$gold)
players$outcome <- factor(players$outcome)
#Matches
matches$case <- as.integer(matches$case)
matches$match <- as.integer(matches$match)
matches$match.type <- factor(matches$match.type)
matches$most.common.offense <- factor(matches$most.common.offense)
matches$reports.allies <- as.integer(matches$reports.allies)
matches$reports.enemies <- as.integer(matches$reports.enemies)
matches$time.played <- as.integer(matches$time.played)

#Removendo possíveis duplicatas(Não me pergunte como elas foram parar ai, ver isso depois)
players <- unique(players)
matches <- unique(matches)

#transformando colunas de categoria em factors.
matches$match.type <- factor(matches$match.type)
matches$most.common.offense <- factor(matches$most.common.offense)

#data.table trabalha com chaves pra melhorar o seu processamento. Aqui eu tou dizendo quais são essas chaves.
setkey(matches,case,match)

setkey(players,case,match,relation.offender)

#Não é usado por nada!
players$champion = NULL

#Criando colunas auxiliares
#Id é um valor sequencial para dar a cada jogador um identificador único
players <- players[,id := seq.int(nrow(players))]
#Casematch é um identificador único para partidas, que nada mais é do que a junção de $case e $match.
players <- players[,casematch := paste(case,match)]
matches <- matches[,casematch := paste(case,match)]
#Count é uma coluna auxiliar para contar a quantidade de jogadores em cada partida. A coluna é completamente preenchida por 1s.
players <- players[,count := rep.int(1,nrow(players))]

#Remoção de partidas inválidas. Uma partida é inválida se:
  #1. Se uma entrada em matches não tiver seu equivalente em players, e vice-versa.   
  #2. relation.offender ou most.common.offense == ""
  #3. Uma partida não tiver 10 jogadores no seu total.
#1
  removal <- setdiff(union(matches$casematch,players$casematch),intersect(matches$casematch,players$casematch))
#2
  removal <- append(removal, players[players$relation.offender == "",casematch])
  removal <- append(removal, matches[matches$most.common.offense == "",casematch])
#3
  removal <- append(removal,players[,.(count = sum(count)), by=casematch][count < 10,casematch])
#Removendo possíveis duplicatas.
removal <- unique(removal)


players <- players[!(players$casematch %in% removal)]
matches <- matches[!(matches$casematch %in% removal)]

matches <- matches[,reports.allies := ifelse(reports.allies==5,4L,reports.allies)]

#Agrupando tipos de ofensa:
#Offensive Language, Verbal abuse -> Verbal offense
#Intentionally feeding, Assisting enemy team -> Helping enemy
#Spamming, Inapropiate name -> Others
matches <- matches[,most.common.offense :=
                                ifelse(most.common.offense=="Assisting Enemy Team" | most.common.offense=="Intentionally Feeding",
                                  "Helping enemy",
                                ifelse(most.common.offense=="Offensive Language" | most.common.offense=="Verbal Abuse",
                                  "Verbal offense",
                                ifelse(most.common.offense=="Inappropriate Name" | most.common.offense=="Spamming",
                                  "Others",
                                "Negative Attitude")))
                  ]

#Assisting Enemy Team, Intentionally Feeding, Offensive Language, Verbal Abuse, Inappropriate Name, Spamming
#Removendo colunas auxiliares que não irão ser mais necessárias.
players$count = NULL
players$casematch = NULL

#Refazendo factors para retirar quaisquer possíveis valores inválidos
players$relation.offender <- factor(players$relation.offender)
matches$most.common.offense <- factor(matches$most.common.offense)
matches$match.type <- factor(matches$match.type)
