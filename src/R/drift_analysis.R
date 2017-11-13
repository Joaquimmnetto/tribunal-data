require(data.table)
setwd("~/PyCharm-Workspace/tribunaldb/")
load("base_data.RData")
source("src/R/utils.R")



r2d_fl = "data/model_drift/lda_sym_15/labels.csv"
topics <- fread(r2d_fl, header = FALSE, sep=',', showProgress=TRUE,
	col.names = c("case", "match", "relation.offender", "timeslice", "topic"),
	colClasses = c("factor", "factor", "factor", "integer", "factor")
)

setkey(topics, case, match, relation.offender, timeslice)

#full/lda_sym_15
{
topics[,topic := factor(
	ifelse(topic==9 | topic==12 | topic==13,
				 "tactics",
				 ifelse(topic==2 | topic==14,
				 			 "complaints",
				ifelse(topic==5, "arguments",
				ifelse(topic==1, "tactics.pos",
				ifelse(topic==6, "small.talk",						 			 
				ifelse(topic==3, "insults",						 			 
				ifelse(topic==4, "taunts",						 			 
				ifelse(topic==7 | topic==8 | topic==10, "other.langs",
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
	agr.group <- rep(1:num.agrs, each = agr.size)
	agr.group <- append(agr.group, rep(num.agrs + 1, nrow(dt) - length(agr.group)))
	
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
	),by = i]
																
	
	colnames(topics.aggr)[2] = col.name
	
	topics.aggr <- topics.aggr[, tactics.full := tactics + tactics.pos]
	topics.aggr <- topics.aggr[, mood := tactics.pos + small.talk]
	topics.aggr <- topics.aggr[, insults.prov := insults + taunts]
	
	topics.aggr <- topics.aggr[, neg := arguments + complaints + insults + taunts]
	topics.aggr <- topics.aggr[, neg := complaints + insults + taunts]
	topics.aggr <- topics.aggr[, pos := small.talk + tactics.full]
	
	return(topics.aggr)
}

ts.aggr = build.topics.aggr(dt = topics, 
														value.col = 'timeslice', topics.col = 'topic',agr.size = 10000)
ts.aggr.offender = build.topics.aggr(dt = topics[relation.offender == 'offender'], 
																		 value.col = 'timeslice', topics.col = 'topic', agr.size = 10000)
ts.aggr.ally = build.topics.aggr(dt = topics[relation.offender == 'ally'], 
																 value.col = 'timeslice', topics.col = 'topic',agr.size = 10000)
ts.aggr.enemy = build.topics.aggr(dt = topics[relation.offender == 'enemy'], 
																	value.col = 'timeslice', topics.col = 'topic',agr.size = 10000)


plot.aggr <- function(dt,title='all'){
	ggplot(dt) + geom_smooth(aes(x = value, y = tactics, color = "Tactics"), span = 0.8) + 
		geom_smooth(aes(x = value, y = tactics.pos, color = "Tactics/Pos"), span = 0.8) + 
		geom_smooth(aes(x = value, y = complaints, color = "Complaints"), span = 0.8) + 
		geom_smooth(aes(x = value, y = arguments, color = "Arguments"), span = 0.8) + 
		geom_smooth(aes(x = value, y = insults, color = "Insults"), span = 0.8) + 
		geom_smooth(aes(x = value, y = taunts, color = "Taunts"), span = 0.8) +
		ggtitle(title) + coord_cartesian(xlim = c(0, 5))
}


#60? Visualmente de acordo com o gráfico de densidade de tempos de partida. 99% dos valores se encaixam nesse intervalo, 
#enquanto 94% se encaixam para 50, e apenas 74% para 40.
#passo 0: definir um escopo de tempo relevante [0,60](0,1,2,3,4,5)

#passo 0.5: mostrar os topicos usados em cada intervalo por coluna, não por linha.
#setkey(groups,case,match,relation.offender)
#topics <- merge(topics, groups[,.(case,match,relation.offender,performance,contamination)], all.x=TRUE, all.y=FALSE)

ts.topics.col <- topics[timeslice == 0,.(case,match,relation.offender,topic)]
setnames(ts.topics.col,'topic','ts.0')
setkey(ts.topics.col, case, match, relation.offender)

for(i in 1:5) {
	ts.topics.col <- merge(ts.topics.col,
												 topics[timeslice == i, .(case,match,relation.offender,topic)], all = TRUE)
	setnames(ts.topics.col,'topic',sprintf('ts.%d',i))
	setkey(ts.topics.col,case,match,relation.offender)
}

setkey(groups, case, match, relation.offender)
ts.topics.col = merge(ts.topics.col,
											groups[,.(case,match,relation.offender,performance,contamination)], 
											all.x = TRUE, all.y = FALSE)


ts.topics.col = merge(ts.topics.col, 
											matches[,.(case,match,time.played)], 
											all.x = TRUE, all.y = FALSE)
setkey(ts.topics.col,case,match,relation.offender)

ts.topics.col = ts.topics.col[, time.played := time.played/60]
ts.topics.col[time.played > 10 & is.na(ts.0), ts.0 := 'empty']
ts.topics.col[time.played > 20 & is.na(ts.1), ts.1 := 'empty']
ts.topics.col[time.played > 30 & is.na(ts.2), ts.2 := 'empty']
ts.topics.col[time.played > 40 & is.na(ts.3), ts.3 := 'empty']
ts.topics.col[time.played > 50 & is.na(ts.4), ts.4 := 'empty']
ts.topics.col[time.played > 60 & is.na(ts.5), ts.5 := 'empty']
setkey(ts.topics.col,case,match,relation.offender)

ts.topics.col[,no.change := FALSE]
ts.topics.col[(ts.0 == ts.1 | is.na(ts.0) | is.na(ts.1))  
							& (ts.1 == ts.2 | is.na(ts.1) | is.na(ts.2))  
							& (ts.2 == ts.3 | is.na(ts.2) | is.na(ts.3))  
							& (ts.3 == ts.4 | is.na(ts.3) | is.na(ts.4)) 
							& (ts.4 == ts.5 | is.na(ts.4) | is.na(ts.5))
							,no.change := TRUE]


#-----------------------arules---------------------------
item.name <- function(str) {
	return(
		gsub(".+=","",
				 gsub("[{}]","",str)
		))
}

lrhs.name <- function(str) {
	return(
		gsub("=.+","",
				 gsub("[{}]","",str)
		))
}

get.perc <- function(lrhs, percs) {
	if(class(lrhs) == "character") {
		items <- item.name(lrhs)
		col.names <- lrhs.name(lrhs)
	}
	else{
		items <- item.name(labels(lrhs))
		col.names <- lrhs.name(labels(lrhs))	
	}
	
	comb.names <- copy(col.names)
	
	for(i in 1:length(items)) {
		comb.names[i] <- paste(col.names[i],items[i],sep = ".")
	}
	
	return(unlist(percs[col.names])[comb.names])
}

supp <- function(dt){
	lhs.name = names(dt)[1]
	rhs.name = names(dt)[2]
	items.names = union(levels(dt[[1]]),levels(dt[[2]]))
	
	results = list()
	for(item in items.names){
		lhs.count = nrow(dt[get(lhs.name) != get(rhs.name),1][get(lhs.name) == item])
		rhs.count = nrow(dt[get(lhs.name) != get(rhs.name),2][get(rhs.name) == item])
		eq.count = nrow(dt[get(lhs.name) == get(rhs.name),1][get(lhs.name) == item])
		results[[item]] = (lhs.count + rhs.count + eq.count)/nrow(dt)
	}
		
	return(results)
}

filter.rules <- function(dt, rules, lift.dist, min.lc, lhs.only=NULL){
	
	percs = list()
	for(name in names(dt)) {
		percs[[name]] = prop.table(summary(dt[,get(name)]))	
	}
	
	library(arules)
	
	rules = subset(rules, subset = (abs(lift - 1) > lift.dist))
	
	
	#supt = supp(dt)
	#lhs.sup = unlist(supt[item.name(labels(rules@lhs))])
	lhs.perc = get.perc(rules@lhs, percs)
	rhs.perc = get.perc(rules@rhs, percs)
	min.perc = pmin(lhs.perc, rhs.perc)
	
	rules@quality$conf.lhs = rules@quality$support/lhs.perc
	rules@quality$conf.rhs = rules@quality$support/rhs.perc
	rules@quality$confidence = rules@quality$support/min.perc
	
	rules = subset(rules, subset = confidence > min.lc)
	
	if(!is.null(lhs.only)) {
  	rules = arules::subset(rules, subset = (lhs %pin% sprintf("%s=%s",names(dt)[1],lhs.only)))
	}
	return(rules)
}

graph_arules <- function(rules) {
	require(visNetwork)
	require(arulesViz)
	ig <- plot( rules, method = "graph" )
	ig_df <- get.data.frame( ig, what = "both" )
	ig_df$vertices = transform(ig_df$vertices, support = c(NA, support[-nrow(ig_df$vertices)]))
	ig_df$vertices = transform(ig_df$vertices, confidence = c(NA, confidence[-nrow(ig_df$vertices)]))
	ig_df$vertices = transform(ig_df$vertices, lift = c(NA, lift[-nrow(ig_df$vertices)]))
	ig_df$vertices = transform(ig_df$vertices, conf.lhs = c(NA, conf.lhs[-nrow(ig_df$vertices)]))
	ig_df$vertices = transform(ig_df$vertices, conf.rhs = c(NA, conf.rhs[-nrow(ig_df$vertices)]))
	
	
	
	return(visNetwork(
		nodes = data.frame(
			id = ig_df$vertices$name
			,value = abs(ig_df$vertices$confidence) # could change to lift or confidence
			,color = ifelse(ig_df$vertices$lift < 1, 'red', 'green')
			,title = ifelse(!is.na(ig_df$vertices$support),
													sprintf("l:%.2f, cl:%.2f, cr:%.2f, lc:%.2f",
											 				ig_df$vertices$lift, 
											 				ig_df$vertices$conf.lhs, 
											 				ig_df$vertices$conf.rhs,
											 				ig_df$vertices$confidence
											 				),
													ig_df$vertices$name
											)
			
			,ig_df$vertices
		)
		, edges = ig_df$edges
	) %>% visEdges(arrows = "to") %>%	visOptions(highlightNearest = T)
	)
}


slices.arules <- function(dts, global.sup = 0.003,
													min.confidence = 0.30, 
													min.lift.dist = 0.30,
													lhs.only=NULL){
	require(arules)
	total.rules = NULL
	if(class(dts) != 'list') {
		dts = list(y1 = dts)
	}
	
	for(dt in dts) {
		rules = apriori(dt,
										parameter = list(confidence = 0, support = global.sup)
		)
		rules = filter.rules(dt, rules, 
												 lift.dist = min.lift.dist, 
												 min.lc = min.confidence,
												 lhs.only = lhs.only
		)
		
		if(is.null(total.rules)) {
			total.rules = rules
		}else{
			total.rules = append(total.rules, rules)
		}
	}
	
	
	if(length(rules) > 0) {
		ruledf = data.table(
			lhs = labels(total.rules@lhs),
			rhs = labels(total.rules@rhs), 
			total.rules@quality)
		graph = graph_arules(total.rules)
		return(list(rules = total.rules, rules.table = ruledf, rules.graph = graph))
	}
	
	return(NULL)
}
verticalize <- function(dt){
	lhs = list(dt[,.(ts.0)],
						 dt[,.(ts.1)],
						 dt[,.(ts.2)],
						 dt[,.(ts.3)],
						 dt[,.(ts.4)]
						 )
	rhs = list(dt[,.(ts.1)],
						 dt[,.(ts.2)],
						 dt[,.(ts.3)],
						 dt[,.(ts.4)],
						 dt[,.(ts.5)]
	)
	trans.topics = rbindlist(lhs)
	trans.topics = cbind(trans.topics,rbindlist(rhs))
	setnames(trans.topics,c("ts.0","ts.1"),c("lhs","rhs"))
	return(trans.topics)
}

compare.groups <- function(dt, group.a, group.b){
	lhs = list(dt[relation.offender == group.a, .(ts.0)],
						 dt[relation.offender == group.a, .(ts.1)],
						 dt[relation.offender == group.a, .(ts.2)],
						 dt[relation.offender == group.a, .(ts.3)],
						 dt[relation.offender == group.a, .(ts.4)],
						 dt[relation.offender == group.a, .(ts.5)]
						)
	rhs = list(dt[relation.offender == group.b, .(ts.0)],
						 dt[relation.offender == group.b, .(ts.1)],
						 dt[relation.offender == group.b, .(ts.2)],
						 dt[relation.offender == group.b, .(ts.3)],
						 dt[relation.offender == group.b, .(ts.4)],
						 dt[relation.offender == group.b, .(ts.5)]
						)
	trans.topics = rbindlist(lhs)
	trans.topics = cbind(trans.topics,rbindlist(rhs))
	names(trans.topics) <- c(group.a,group.b)
	return(trans.topics)
}
dt = merge(groups[relation.offender == 'offender', .(case, match, topic)], 
					 groups[relation.offender == 'ally', .(case, match, topic)], 
					 by = c('case','match'))
rules = slices.arules(dt[,.(topic.x,topic.y)], 
											min.confidence = 0.1, min.lift.dist = 0.3, lhs.only = "")
inspectDT(rules$rules)
rules$rules.graph 
#%>% visPhysics(barnesHut=list(springLength=500)) %>%
#	visHierarchicalLayout(direction = "LR", sortMethod="directed", levelSeparation = 600)



#Arvore
require(rpart) 
require(rattle)


fit01.full <- rpart(ts.1 ~ ts.0 + performance + contamination, data = ts.topics.col)
fit12.full <- rpart(ts.2 ~ ts.1 + performance + contamination, data = ts.topics.col)
fit23.full <- rpart(ts.3 ~ ts.2 + performance + contamination, data = ts.topics.col)
fit34.full <- rpart(ts.4 ~ ts.3 + performance + contamination, data = ts.topics.col)
fit45.full <- rpart(ts.5 ~ ts.4 + performance + contamination, data = ts.topics.col)


# fit.ae <- rpart(ts.1 ~ ts.0 + performance + contamination, data=ts.topics.col[relation.offender!='offender'])
# fit.of <- rpart(ts.1 ~ ts.0 + performance + contamination, data=ts.topics.col[relation.offender=='offender'])
# fit.a <- rpart(ts.1 ~ ts.0 + performance + contamination, data=ts.topics.col[relation.offender=='ally'])
# fit.e <- rpart(ts.1 ~ ts.0 + performance + contamination, data=ts.topics.col[relation.offender=='enemy'])
# 
# fit.nc <- rpart(ts.1 ~ ts.0 + performance + contamination, data=ts.topics.col[relation.offender=='enemy' & contamination == 0] )
# fit.ce <- rpart(ts.1 ~ ts.0 + performance + contamination, data=ts.topics.col[relation.offender=='enemy' & contamination > 0] )


# results = slices.arules(ts.topics.col[ts.0!=ts.1 | ts.1!=ts.2 | ts.0!=ts.2, .(ts.0,ts.1,ts.2)], 
# 													min.confidence = 0.30, min.lift.dist = 0.30)
# View(results$rules.table)
# results$rules.graph

#Porcentagem de partidas com topicos iguais:
#ts0 a ts1	#ts0 a ts2	#ts0 a ts3	#ts0 a ts4	#ts0 a ts5
#0.36251		#0.1835695	#0.142846		#0.1342556	#0.1330021

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