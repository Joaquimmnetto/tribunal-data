require(data.table)
setwd("~/PyCharm-Workspace/tribunaldb/")
load("base_data.RData")
source("src/R/utils.R")



dataset="model_drift"
r2d_fl = paste("data/",dataset,"/r2d.csv", sep='')
topics <- fread(r2d_fl, header = FALSE, sep=',', showProgress=TRUE,
	col.names = c("case", "match", "relation.offender", "timeslice","topic"),
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

create_ts_data_row <- function(dt,ts) {
	count <- length(dt[timeslice==ts]$topic)
	row <- data.table(t(prop.table(summary(dt[timeslice==ts]$topic))),t(prop.table(summary(dt[timeslice==ts]$topic.2)))
										,timeslice=ts, count=count)
	return(row)
}

create_ts_data <- function(dt,max_ts=10){
	ts_data <- create_ts_data_row(dt,0)
	for(ts in 1:max_ts){
		row <- create_ts_data_row(dt,ts)
		ts_data<- rbind(ts_data,row,fill=TRUE)
	}
	return(ts_data)
}

ts.data <- create_ts_data(topics,max_ts=5)


ggplot(ts.data) + geom_line(aes(x=timeslice, y=tactics),color='red' ) + geom_point(aes(x=timeslice, y=tactics)) + 
									geom_line(aes(x=timeslice, y=tactics.pos, color='green')) + geom_point(aes(x=timeslice, y=tactics.pos)) +
									geom_line(aes(x=timeslice, y=complaints, color='blue')) + geom_point(aes(x=timeslice, y=complaints)) +
									geom_line(aes(x=timeslice, y=arguments, color='yellow')) + geom_point(aes(x=timeslice, y=arguments)) +
									geom_line(aes(x=timeslice, y=insults, color='black')) + geom_point(aes(x=timeslice, y=insults)) +
									geom_line(aes(x=timeslice, y=taunts, color='white')) + geom_point(aes(x=timeslice, y=taunts)) + ggtitle("offender")

hist(topics$timeslice)

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


ggplot(ts.aggr) + geom_smooth(aes(x=value, y=tactics), color='red') + geom_tile(aes(x=value, y=tactics),color='red') +
									geom_smooth(aes(x=value, y=tactics.pos), color='green') + geom_tile(aes(x=value, y=tactics.pos), color='green') +
									geom_smooth(aes(x=value, y=complaints), color='yellow') + geom_tile(aes(x=value, y=complaints), color='yellow') +
									geom_smooth(aes(x=value, y=arguments), color='blue') + geom_tile(aes(x=value, y=arguments), color='blue') +
									geom_smooth(aes(x=value, y=insults), color='black') + geom_tile(aes(x=value, y=insults),color='black') +
									geom_smooth(aes(x=value, y=taunts), color='#FF00FF') + geom_tile(aes(x=value, y=taunts),color='#FF00FF') +
								 coord_cartesian(xlim=c(0, 5))
	
ggplot(ts.aggr) + geom_smooth(aes(x=value, y=pos),color='red') + geom_tile(aes(x=value, y=pos),color='red') +
	geom_smooth(aes(x=value, y=neg),color='green') + geom_tile(aes(x=value, y=neg), color='green') +
	coord_cartesian(xlim=c(0, 5))

ggplot(ts.data) + geom_line(aes(x=timeslice, y=positive),color='red' ) + geom_point(aes(x=timeslice, y=positive),color='red') + 
	geom_line(aes(x=timeslice, y=negative),color='green') + geom_point(aes(x=timeslice, y=negative),color='green')

	
	#geom_smooth(aes(x=value, y=tactics.pos, color='green')) + geom_point(aes(x=value, y=tactics.pos, alpha=0.01)) +
	#geom_smooth(aes(x=value, y=complaints, color='blue')) + geom_point(aes(x=value, y=complaints, alpha=0.01)) +
	#geom_smooth(aes(x=value, y=arguments, color='yellow')) + geom_point(aes(x=value, y=arguments, alpha=0.01)) +
	#geom_smooth(aes(x=value, y=insults, color='black')) + geom_point(aes(x=value, y=insults, alpha=0.01)) +
	#geom_smooth(aes(x=value, y=taunts, color='white')) + geom_point(aes(x=value, y=taunts, alpha=0.01))

#60? Visualmente de acordo com o gráfico de densidade de tempos de partida. 99% dos valores se encaixam nesse intervalo, 
#enquanto 94% se encaixam para 50, e apenas 74% para 40.
#passo 0: definir um escopo de tempo relevante [0,60](0,1,2,3,4,5)
ts.topics <- topics[timeslice < 6]

#passo 0.5: mostrar os topicos usados em cada intervalo por coluna, não por linha.
ts.topics.col <- ts.topics[timeslice==0,.(case,match,relation.offender,topic)]
setnames(ts.topics.col,'topic','ts.0')
setkey(ts.topics.col,case,match,relation.offender)

for(i in 1:5){
	ts.topics.col <- merge(ts.topics.col,ts.topics[timeslice==i,.(case,match,relation.offender,topic)],all=TRUE)
	setnames(ts.topics.col,'topic',sprintf('ts.%d',i))
	setkey(ts.topics.col,case,match,relation.offender)
}

#Passo 1: apriori para verificar quais são os drifts.
require(arules)
ap.results <- apriori(ts.topics.col[relation.offender=='offender',.(ts.1,ts.2,ts.3,ts.4,ts.5)],parameter=list(confidence=0.01,target='rules'))
inspect(ap.results,by='lift')

#apriori(ts.topics.col[relation.offender=='enemy',.(ts.1,ts.2,ts.3,ts.4,ts.5)],parameter=list(confidence=0.40,target='rules'))
#inspect(head(ap.results,by='lift'))

#passo 2: remover partidas aonde não há drift, já que elas não nos interessam(não há mudança de tópicos durante a partida)
	#não parece realmente necessario no momento

#passo 3: plotar partidas que driftam e verificar quais são as tendências.

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