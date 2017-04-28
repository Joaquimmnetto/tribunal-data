#install.packages('dplyr')
#install.packages('dtplyr')
#install.packages('data.table')
require(dplyr)
require(dtplyr)
require(data.table)

args <- commandArgs(trailingOnly=TRUE)
args[1] <- 'full'
print(args)
setwd(paste('~/PyCharm-Workspace/tribunaldb/data/',args[1],sep=''))
print(getwd())
players_fl <- "players.csv"
matches_fl <- "matches.csv"
chat_fl <- "chat.csv"

#Problemas na construção do csv:
#1. Duplicação de dados
#2. matches e players com partidas disjuntas.

#-----------------Carregamento dos dados e pré-processamento-----------------------------

#Carregando dados...
#Alguns dados estão disjuntos(matches sem players equivalentes e vice-versa) ver issaí. Por enquanto só retirando esses casos do dataset.
#Carregando e cortando o chat primeiro para tudo caber na memória
chat <- setDT(fread(chat_fl, header = FALSE, sep=',', showProgress=TRUE, 
                    colClasses = c("factor","factor","NULL","NULL","NULL","NULL")))
setnames(chat, names(chat), c("case", "match"))
chat <- unique(chat)

players <- setDT(fread(players_fl, header = FALSE, sep=',', showProgress=TRUE,
                       col.names = c("case", "match", "relation.offender", "champion", 
                                     "kills", "deaths","assists", "gold", "outcome"),
                       colClasses = c("factor", "factor", "factor", "factor",
                                      "integer", "integer", "integer","integer", "factor")))
matches <- setDT(fread(matches_fl, header = FALSE, sep=',', showProgress=TRUE, 
                       col.names = c("case", "match", "match.type", "most.common.offense",
                                     'report.text.allies', 'report.text.enemies',
                                     "reports.allies", "reports.enemies", "time.played"), 
                       colClasses = c("factor", "factor", "factor", "factor",
                                      "character","character",
                                      "integer", "integer", "integer")))

#Removendo possíveis duplicatas(Não me pergunte como elas foram parar ai, ver isso depois)
players <- unique(players)
matches <- unique(matches)

#data.table trabalha com chaves pra melhorar o seu processamento. Aqui eu tou dizendo quais são essas chaves.
setkey(matches,case,match)
setkey(players,case,match,relation.offender)

#Não é usado por nada!
#players$champion = NULL

#Criando colunas auxiliares
#Id é um valor sequencial para dar a cada jogador um identificador único
#players <- players[,id := seq.int(nrow(players))]
#Casematch é um identificador único para partidas, que nada mais é do que a junção de $case e $match.
players <- players[,casematch := paste(case,match)]
matches <- matches[,casematch := paste(case,match)]
chat <- chat[,casematch := paste(case,match)]
#Count é uma coluna auxiliar para contar a quantidade de jogadores em cada partida. A coluna é completamente preenchida por 1s.
players <- players[,count := rep.int(1,nrow(players))]


num.players = 10 #para full
if(grepl('ally',args[1])){
	num.players = 4
}else if(grepl('enemy',args[1])){
	num.players = 5
}else if(grepl('offender',args[1])){
	num.players = 1
}
print(num.players)

#Remoção de partidas inválidas. Uma partida é inválida se:
  #1. Se uma entrada em matches não tiver seu equivalente em players, ou chat e vice-versa.   
  #2. relation.offender ou most.common.offense == ""
  #3. Uma partida não tiver 10 jogadores no seu total.
#1
  removal <- setdiff(union(union(matches$casematch, players$casematch), chat$casematch), 
                     intersect(intersect(matches$casematch, players$casematch), chat$casematch))
#2
  removal <- append(removal, players[players$relation.offender == "",casematch])
  removal <- append(removal, matches[matches$most.common.offense == "",casematch])
#3
  removal <- append(removal,players[,.(count = sum(count)), by=casematch][count < num.players, casematch])
  
#Removendo possíveis duplicatas.
removal <- unique(removal)
print(length(removal))

players <- players[!(casematch %in% removal)]
matches <- matches[!(casematch %in% removal)]
chat <- chat[!(casematch %in% removal)]

#Transformandos possíveis reports de aliados == 5 em == 4! 
#Provavelmente aconteceu em casos antes da rito gomes implementar a restrição
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

matches$casematch <- NULL

valid.matches <- chat
rm(chat)

fwrite(matches,file = "matches.csv", col.names = FALSE)
fwrite(players,file = "players.csv", col.names = FALSE)
fwrite(valid.matches, file="valid_matches.csv", col.names = FALSE)

rm(matches)
rm(players)
rm(removal)


# matches <- setDT(fread(matches_fl, header = TRUE, sep=',', showProgress=TRUE, 
#                        col.names = c("case",'match','casematch'), 
#                        colClasses = c("NULL","NULL",'factor')))
valid.matches$case=NULL
valid.matches$match=NULL

system(paste('split -d -l 50000000 ',chat_fl, ' _xxx',sep=''))

for(i in 0:10000){
  if(i < 10){
    part_fl = paste('_xxx0',i, sep='')
  }else{
    part_fl = paste('_xxx',i, sep='')
  }
  if(!file.exists(part_fl)){
    break
  }
  
  chat <- setDT(fread(part_fl, header = TRUE, sep=',', showProgress=TRUE, 
                      col.names = c("case",'match','relation.offender','champion','time','message'), 
                      colClasses = c("factor","factor",'factor','factor','character','character')))
  
  chat <- chat[,casematch := paste(case,match)]
  chat$casematch <- factor(chat$casematch)
  chat <- chat[(casematch %in% valid.matches$casematch)]
  chat$casematch <- NULL
  system(paste('rm',part_fl))
  
  fwrite(chat, paste('chat.',i,'.csv_part',sep=''), col.names = FALSE)
}
system('rm chat.csv')
system('cat *.csv_part >> chat.csv')
system('rm *.csv_part')

#Adcionando informações dos grupos construídos com LDA
#matches <- load.group.labels("ally")
#matches <- load.group.labels("enemy")
#matches <- load.group.labels("offender")
#matches <- load.group.labels("full")
