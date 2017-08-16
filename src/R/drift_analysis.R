require(data.table)
setwd("~/PyCharm-Workspace/tribunaldb/")
load("base_data.RData")
source("src/R/utils.R")



dataset="model_drift"
r2d_fl = paste("data/",dataset,"/r2d.csv", sep='')
topics <- fread(r2d_fl, header = FALSE, sep=',', showProgress=TRUE,
	col.names = c("case", "match", "relation.offender", "timeslice", "topic"),
	colClasses = c("factor", "factor", "factor", "integer", "factor")
)

setkey(topics, case, match, relation.offender, timeslice)
{
topics[,topic := factor(
	ifelse(topic==10 | topic==12,
				 "tactics",
				 ifelse(topic==4 | topic==7,
				 			 "complaints",
				ifelse(topic==5, "arguments",
				ifelse(topic==1 | topic==9, "tactics.pos",
				ifelse(topic==2, "small.talk",						 			 
				ifelse(topic==3, "insults",						 			 
				ifelse(topic==0, "taunts",						 			 
				ifelse(topic==8 | topic==11 | topic==13, "other.langs",
				"other")))))))))
	]

topics[,topic.2 := factor(ifelse
														(topic=='tactics'|topic=='tactics.pos'|topic=='small.talk',
															'positive',
													ifelse
															(topic=='complaints'|topic=='arguments'|topic=='insults'|topic=='taunts',
															'negative',
													NA
													))
	
	
		)]
}

build.topics.aggr <- function(dt = topics, value.col, topics.col, col.name = 'value', agr.size = 10000){
	num.agrs = as.integer((nrow(dt)/agr.size))
	agr.group <- rep(1:num.agrs, each=agr.size)
	agr.group <- append(agr.group, rep(num.agrs+1, nrow(dt)-length(agr.group)))
	
	topics.aggr <- dt[,.(value = get(value.col), topics = get(topics.col))]
	topics.aggr <- topics.aggr[order(value)]
	topics.aggr <- topics.aggr[,i := agr.group]
	topics.aggr <- topics.aggr[,.(value = mean(value),
																"arguments" = prop.table(summary(topics))['arguments'],
																"complaints" = prop.table(summary(topics))['complaints'],
																"insults" = prop.table(summary(topics))['insults'],
																"small.talk" = prop.table(summary(topics))['small.talk'],
																"taunts" = prop.table(summary(topics))['taunts'],
																"tactics" = prop.table(summary(topics))['tactics'],
																"tactics.pos" = prop.table(summary(topics))['tactics.pos'],
																"other.langs" = prop.table(summary(topics))['other.langs'],
																"nas" = prop.table(summary(topics))["NA's"]
	),by=i]
																
	
	colnames(topics.aggr)[2] = col.name
	
	topics.aggr <- topics.aggr[, tactics.full := tactics + tactics.pos]
	topics.aggr <- topics.aggr[, mood := tactics.pos + small.talk]
	topics.aggr <- topics.aggr[, insults.prov := insults + taunts]
	
	topics.aggr <- topics.aggr[, neg := arguments + complaints + insults + taunts]
	topics.aggr <- topics.aggr[, neg := complaints + insults + taunts]
	topics.aggr <- topics.aggr[, pos := small.talk + tactics.full]
	
	return(topics.aggr)
}

ts.aggr = build.topics.aggr(dt=topics, value.col='timeslice', topics.col='topic',agr.size = 10000)
ts.aggr.offender = build.topics.aggr(dt=topics[relation.offender=='offender'], value.col='timeslice', topics.col='topic',agr.size = 10000)
ts.aggr.ally = build.topics.aggr(dt=topics[relation.offender=='ally'], value.col='timeslice', topics.col='topic',agr.size = 10000)
ts.aggr.enemy = build.topics.aggr(dt=topics[relation.offender=='enemy'], value.col='timeslice', topics.col='topic',agr.size = 10000)


plot.aggr <- function(dt,title='all'){
	ggplot(dt) + geom_smooth(aes(x=value, y=tactics, color="Tactics"), span=0.8) + 
		geom_smooth(aes(x=value, y=tactics.pos, color="Tactics/Pos"), span=0.8) + 
		geom_smooth(aes(x=value, y=complaints, color="Complaints"), span=0.8) + 
		geom_smooth(aes(x=value, y=arguments, color="Arguments"), span=0.8) + 
		geom_smooth(aes(x=value, y=insults, color="Insults"), span=0.8) + 
		geom_smooth(aes(x=value, y=taunts, color="Taunts"), span=0.8) +
		ggtitle(title) + coord_cartesian(xlim=c(0, 5))
}


#60? Visualmente de acordo com o gráfico de densidade de tempos de partida. 99% dos valores se encaixam nesse intervalo, 
#enquanto 94% se encaixam para 50, e apenas 74% para 40.
#passo 0: definir um escopo de tempo relevante [0,60](0,1,2,3,4,5)

#passo 0.5: mostrar os topicos usados em cada intervalo por coluna, não por linha.
ts.topics.col <- topics[timeslice < 6][timeslice==0,.(case,match,relation.offender,topic)]
setnames(ts.topics.col,'topic','ts.0')
setkey(ts.topics.col,case,match,relation.offender)

for(i in 1:5){
	ts.topics.col <- merge(ts.topics.col,ts.topics[timeslice==i,.(case,match,relation.offender,topic)],all=TRUE)
	setnames(ts.topics.col,'topic',sprintf('ts.%d',i))
	setkey(ts.topics.col,case,match,relation.offender)
}
ts.topics.col = ts.topics.col[matches[,.(case,match,time.played)]]
ts.topics.col[time.played > 10 & is.na(ts.0), ts.0 := 'empty']
ts.topics.col[time.played > 20 & is.na(ts.1), ts.1 := 'empty']
ts.topics.col[time.played > 30 & is.na(ts.2), ts.2 := 'empty']
ts.topics.col[time.played > 40 & is.na(ts.3), ts.3 := 'empty']
ts.topics.col[time.played > 50 & is.na(ts.4), ts.4 := 'empty']
ts.topics.col[time.played > 60 & is.na(ts.5), ts.5 := 'empty']


#Passo 1: apriori para verificar quais são as mudanças
require(arules)
ap.all <- apriori(ts.topics.col[,.(ts.0,ts.1,ts.2,ts.3,ts.4,ts.5)] ,
											parameter=list(confidence=0.5, support=0.05, target='rules'))
inspect(sort(ap.all, by='lift'))rm()


#apriori(ts.topics.col[relation.offender=='enemy',.(ts.1,ts.2,ts.3,ts.4,ts.5)],parameter=list(confidence=0.40,target='rules'))
#inspect(head(ap.results,by='lift'))

#passo 1.5: Quantificar partidas aonde não há mudanças
ts.topics.col[,no.change:=FALSE]
ts.topics.col[(ts.0 == ts.1 | is.na(ts.0) | is.na(ts.1))  
											 & (ts.1 == ts.2 | is.na(ts.1) | is.na(ts.2))  
											 & (ts.2 == ts.3 | is.na(ts.2) | is.na(ts.3))  
											 & (ts.3 == ts.4 | is.na(ts.3) | is.na(ts.4)) 
											 & (ts.4 == ts.5 | is.na(ts.4) | is.na(ts.5))
												,no.change := TRUE]
									
#Porcentagem de partidas com topicos iguais:
#ts0 a ts1	#ts0 a ts2	#ts0 a ts3	#ts0 a ts4	#ts0 a ts5
#0.36251		#0.1835695	#0.142846		#0.1342556	#0.1330021

#passo 2: remover partidas aonde não há mudanças, já que elas não nos interessam(não há mudança de tópicos durante a partida)
	#não parece realmente necessario no momento.

#passo 3: plotar partidas que driftam e verificar quais são as tendências.
#ggplot(data=ts.topics.col[no.change==FALSE]) 


#passo 4: Procurar e confirmar a existência de um ponto específico aonde o ofensor começa a apresentar comportamento tóxico.

#		0: 0.05220415285872091 - Taunts,			 			 			 			 			 			 			 
# 	1: 0.07854360295331327 - Tactics/Pos,
# 	2: 0.1376437930903135 - small talk,
# 	3: 0.0815565522670425 - insults,
# 	4: 0.09118699926357622 - complaints,
# 	5: 0.1603257246790843 - arguments,
# 	6: 0.00033726304295382114 - ruido,
# 	7: 0.05607255996140124 - complaints,
# 	8: 0.0031807872751050672 - other langs.(ptbr),
# 	9: 0.06443509630645386 - tactics/pos,
# 	10: 0.14012406518620094 - tactics,
# 	11: 0.03536540268413769 - other langs.(es),
# 	12: 0.09501334768089996 - tactics,
# 	13: 0.004010652750796735 - other langs.(chingchong)