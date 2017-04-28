require(data.table)


	rel.ofndr <- "full"
	require(rPython)
	groups <- pkl2R(paste("'data/",rel.ofndr,"/lda_labels_10.pkl'", sep=''))
	r2d <- pkl2R(paste("'data/",rel.ofndr,"/cnt_team_r2d.pkl'", sep=''))
	
	groups <- cbind(data.table(t(matrix(unlist(r2d), nrow=length(unlist(r2d[1]))))),as.data.table(groups))
	rm(r2d)
	
	
	names(groups) <- c("case","match","relation.offender","groups")
	setkey(groups, case,match)
	#2177488
	#1963475
	matches <- merge(matches,
								 groups[relation.offender == 'ally'
											][,ally.groups := factor(groups)
											][,c('relation.offender','groups') := NULL]
								 , all.x=TRUE)
	matches <- merge(matches,
									 groups[relation.offender == 'enemy'
									 			 ][,enemy.groups := factor(groups)
									 			 	][,c('relation.offender','groups') := NULL]
									 , all.x=TRUE)
	matches <- merge(matches,
									 groups[relation.offender == 'offender'
									 			 ][,offender.groups := factor(groups)
									 			 	][,c('relation.offender','groups') := NULL]
									 , all.x=TRUE)
	rm(groups)
	
	matches <- matches[,ally.groups := factor(
						ifelse(ally.groups==0 | ally.groups==9,
							 				 							"tactics",
						 ifelse(ally.groups==2 | ally.groups==3,
							 			 								"complaints",
						 ifelse(ally.groups==4, "arguments",
						 ifelse(ally.groups==5, "tactics.pos",
						 ifelse(ally.groups==6, "chit.chat",						 			 
						 ifelse(ally.groups==7, "insults",						 			 
						 ifelse(ally.groups==8, "provoking",						 			 
						 ifelse(ally.groups==1, "other.langs",
						 			 									NA)))))))))
						]
	matches <- matches[,enemy.groups := factor(
		ifelse(enemy.groups==0 | enemy.groups==9,
					 													"tactics",
					 	ifelse(enemy.groups==2 | enemy.groups==3,
					 			 										"complaints",
		 			 	ifelse(enemy.groups==4, "arguments",
					 	ifelse(enemy.groups==5, "tactics.pos",
						ifelse(enemy.groups==6, "chit.chat",						 			 
						ifelse(enemy.groups==7, "insults",						 			 
						ifelse(enemy.groups==8, "provoking",						 			 
						ifelse(enemy.groups==1, "other.langs",
																		NA)))))))))
		]

	matches <- matches[,offender.groups := factor(
						ifelse(offender.groups==0 | offender.groups==9,
					 													"tactics",
					 	ifelse(offender.groups==2 | offender.groups==3,
					 			 										"complaints",
					 	ifelse(offender.groups==4, "arguments",
					 	ifelse(offender.groups==5, "tactics.pos",
					 	ifelse(offender.groups==6, "chit.chat",						 			 
					 	ifelse(offender.groups==7, "insults",						 			 
					 	ifelse(offender.groups==8, "provoking",						 			 
					 	ifelse(offender.groups==1, "other.langs",
					 													NA)))))))))
]

	
postprocessing <- function(df){
		df <- df[, tactics.full := tactics + tactics.pos]
		df <- df[, mood := tactics.pos + chit.chat]
		df <- df[, insults.prov := insults + provoking]
		
		df <- df[, neg := arguments + complaints + insults + provoking]
		df <- df[, pos := chit.chat + tactics.full]
		
		return(df)
}

build.topics.aggr <- function(value.col, topics.col, agr.size = 10000){
	num.agrs = as.integer((nrow(matches)/agr.size))
	agr.group <- rep(1:num.agrs, each=agr.size)
	agr.group <- append(agr.group, rep(num.agrs+1, nrow(matches)-length(agr.group)))
	
	topics.aggr <- matches[,.(values = get(value.col), topics = get(topics.col))]
	topics.aggr <- topics.aggr[order(values)]
	topics.aggr <- topics.aggr[,i := agr.group]
	topics.aggr <- topics.aggr[,.(values = mean(values),
																"arguments" = prop.table(summary(topics))['arguments'],
																"complaints" = prop.table(summary(topics))['complaints'],
																"insults" = prop.table(summary(topics))['insults'],
																"chit.chat" = prop.table(summary(topics))['chit.chat'],
																"provoking" = prop.table(summary(topics))['provoking'],
																"tactics" = prop.table(summary(topics))['tactics'],
																"tactics.pos" = prop.table(summary(topics))['tactics.pos'],
																"other.langs" = prop.table(summary(topics))['other.langs'],
																"nas" = prop.table(summary(topics))["NA's"]
															),by=i]
	topics.aggr <- postprocessing(topics.aggr)
	
	return(topics.aggr)
}

ally.topics.cont <- build.topics.aggr('ally.contamination','ally.groups')
colnames(ally.topics.cont)[2] = 'contamination'
ally.topics.cont <- ally.topics.cont[,relation.offender := 'ally']

enemy.topics.cont <- build.topics.aggr('enemy.contamination','enemy.groups')
colnames(enemy.topics.cont)[2] = 'contamination'
enemy.topics.cont <- enemy.topics.cont[,relation.offender := 'enemy']

topics.cont <- rbind(ally.topics.cont,enemy.topics.cont)

ally.topics.perf <- build.topics.aggr('ally.performance','ally.groups')
colnames(ally.topics.perf)[2] = 'performance'
ally.topics.perf <- ally.topics.perf[,relation.offender := 'ally']

enemy.topics.perf <- build.topics.aggr('enemy.performance','enemy.groups')
colnames(enemy.topics.perf)[2] = 'performance'
enemy.topics.perf <- enemy.topics.perf[,relation.offender := 'enemy']

offender.topics.perf <- build.topics.aggr('offender.performance','offender.groups')
colnames(offender.topics.perf)[2] = 'performance'
offender.topics.perf <- offender.topics.perf[,relation.offender := 'offender']

topics.perf <- rbind(ally.topics.perf, enemy.topics.perf, offender.topics.perf)

ggplot(data=topics.perf, 
			 aes(x=performance, y=neg, shape=relation.offender)) + 
	geom_point() + geom_smooth(aes(color=relation.offender))
	#labs(x='Group Contamination',y='Tactics + Tactics/Pos', color='Groups')

ggplot(data=topics.cont, 
			 aes(x=contamination,y=neg, color=relation.offender)) + 
	geom_point() + geom_smooth(aes(x=jitter(contamination)))
	labs(x='Group Contamination',y='Tactics + Tactics/Pos', color='Groups')


fwrite(matches[,.(case, match, ally.groups, enemy.groups, offender.groups)],'data\full\groups_labels_lda.csv',col.names = FALSE)


med.t.test <- function(x,not_x){
	print("mean/sd x")
	print(mean(x))
	print(sd(x))
	print("mean/sd y")
	print(mean(not_x))
	print(sd(not_x))
	t.test(x,not_x)
}


#df <- df[, neg := arguments + complaints + insults + provoking]
matches.pos.ally <- matches[ally.groups=='chit.chat' | ally.groups=='tactics' | ally.groups=='tactics.pos']
matches.neg.ally <- matches[ally.groups=='arguments' | ally.groups=='complaints' | ally.groups=='insults' | ally.groups=='provoking']
med.t.test(matches.pos.ally$ally.performance, matches.neg.ally$ally.performance)

matches.pos.enemy <- matches[enemy.groups=='chit.chat' | enemy.groups=='tactics' | enemy.groups=='tactics.pos']
matches.neg.enemy <- matches[enemy.groups=='arguments' | enemy.groups=='complaints' | enemy.groups=='insults' | enemy.groups=='provoking']
med.t.test(matches.pos.enemy$enemy.performance, matches.neg.enemy$enemy.performance)

matches.pos.offender <- matches[offender.groups=='chit.chat' | offender.groups=='tactics' | offender.groups=='tactics.pos']
matches.neg.offender <- matches[offender.groups=='arguments' | offender.groups=='complaints' | offender.groups=='insults' | offender.groups=='provoking']
med.t.test(matches.pos.offender$offender.performance, matches.neg.offender$offender.performance)

med.t.test(matches[enemy.contamination >= 0.75]$enemy.performance,matches[enemy.contamination >= 0.75]$ally.performance)

#Template para testes-t
x <- matches[offender.groups=='tactics' | offender.groups=='tactics.pos']$offender.performance
not_x <- matches[offender.groups!='tactics' & offender.groups!='tactics.pos']$offender.performance
med.t.test(x,not_x)

matches.apriori <- as.data.frame(matches[,c('ally.groups', 'offender.groups')])


rules <- apriori(matches.apriori, 
								 parameter = list(supp=0.001, conf=0.4))


chat_fl <- 'data/chat_targets.csv'
chat_targets <- setDT(fread(chat_fl, header = FALSE, sep=',', showProgress=TRUE,
											 col.names = c("case", "match", "relation.offender", "champion", 
											 							"target"),
											 colClasses = c("factor", "factor", "factor", "factor",
											 							 "factor", "NULL")))

chat_targets_all <- chat_targets[target=='All',(count_all = .N), by=.(case,match,relation.offender)]
chat_targets_cnt <- chat_targets[,(count_all = .N), by=.(case,match,relation.offender)]



matches[ally.groups=='chit.chat' , ally.groups.2 :='Positive'] 
matches[ally.groups=='tactics.pos' , ally.groups.2 :='Positive']
matches[ally.groups=='tactics' , ally.groups.2 :='Positive']
matches[ally.groups=='arguments',ally.groups.2 := 'Negative']
matches[ally.groups=='complaints',ally.groups.2 := 'Negative']
matches[ally.groups=='insults',ally.groups.2 := 'Negative']
matches[ally.groups=='provoking',ally.groups.2 := 'Negative']
matches[,ally.groups.2 := factor(ally.groups.2)]

ggplot(matches) + 
	geom_histogram(aes(x=ally.contamination, fill=ally.groups.2), bins=5,position='fill')+
	labs(x='Ally Performance',y='%', fill='Topics')

matches[enemy.groups=='chit.chat' , enemy.groups.2 :='Positive'] 
matches[enemy.groups=='tactics.pos' , enemy.groups.2 :='Positive']
matches[enemy.groups=='tactics' , enemy.groups.2 :='Positive']
matches[enemy.groups=='arguments',enemy.groups.2 := 'Negative']
matches[enemy.groups=='complaints',enemy.groups.2 := 'Negative']
matches[enemy.groups=='insults',enemy.groups.2 := 'Negative']
matches[enemy.groups=='provoking',enemy.groups.2 := 'Negative']
matches[,enemy.groups.2 := factor(enemy.groups.2)]

ggplot(matches) + 
	geom_histogram(aes(x=enemy.contamination, fill=enemy.groups.2), bins=5,position='fill')+
	labs(x='Enemy Contamination',y='%', fill='Topics')


matches[offender.groups=='chit.chat' , offender.groups.2 :='Positive'] 
matches[offender.groups=='tactics.pos' , offender.groups.2 :='Positive']
matches[offender.groups=='tactics' , offender.groups.2 :='Positive']
matches[offender.groups=='arguments',offender.groups.2 := 'Negative']
matches[offender.groups=='complaints',offender.groups.2 := 'Negative']
matches[offender.groups=='insults',offender.groups.2 := 'Negative']
matches[offender.groups=='provoking',offender.groups.2 := 'Negative']
matches[,offender.groups.2 := factor(offender.groups.2)]


matches[enemy.groups=='chit.chat', enemy.groups.2 :='Small Talk'] 
#matches[enemy.groups=='tactics' | enemy.groups=='tactics.pos', enemy.groups.2 :='Tactics/All']
matches[enemy.groups=='arguments' | enemy.groups=='complaints' | enemy.groups=='insults' | enemy.groups=='provoking', enemy.groups.2 := 'Negative']

ggplot(matches) + 
	geom_histogram(aes(x=enemy.performance, fill=enemy.groups.2), bins=5,position='fill')+
	labs(x='Enemy Performance',y='%', fill='Topics')

ggplot(matches) + 
	geom_histogram(aes(x=enemy.performance, fill=enemy.groups), bins=5,position='fill')+
	labs(x='Enemy Performance',y='%', fill='Topics')


prop.table(summary(matches[ally.contamination <= 0.25]$ally.groups))
prop.table(summary(matches[ally.contamination >= 0.75]$ally.groups))
prop.table(summary(matches[enemy.contamination >= 0.5]$enemy.groups))

ggplot(data=topics.perf, 
			 aes(x=performance, y=pos, shape=relation.offender)) + 
	geom_point() + geom_smooth(aes(color=relation.offender)) +
	labs(x='Group Performance',y='Positive Topics', color='Groups', shape="Groups")

correlation.tests.perf <- function(topic){
		print("Correlation tests for performance")
		print('for ally:')
		x <- with(ally.topics.perf, cor.test(performance, get(topic), method = 'kendall'))
		print(append(x$p.value,x$estimate))
		
		print('for enemy:')
		x <- with(enemy.topics.perf, cor.test(performance, get(topic), method = 'kendall'))
		print(append(x$p.value,x$estimate))
		
		print('for offender:')
		x <- with(offender.topics.perf, cor.test(performance, get(topic), method = 'kendall'))
		print(append(x$p.value,x$estimate))
}

correlation.tests.cont <- function(topic){
	print("Correlation tests for contamination")
	print('for ally:')
	x <- with(ally.topics.cont, cor.test(contamination, get(topic), method = 'kendall'))
	print(append(x$p.value,x$estimate))
	
	print('for enemy:')
	x <- with(enemy.topics.cont, cor.test(contamination, get(topic), method = 'kendall'))
	print(append(x$p.value,x$estimate))
	
}

correlation.tests <- function(topic){
	correlation.tests.perf(topic)
	correlation.tests.cont(topic)
}

correlation.tests('pos')

ggplot(data=topics.cont, 
			 aes(x=contamination, y=pos, shape=relation.offender)) + 
	geom_point() + geom_smooth(aes(x=jitter(contamination), color=relation.offender)) +
	labs(x='Group Performance',y='Positive Topics', color='Groups', shape="Groups")

with(ally.topics.cont, cor.test(contamination, pos, method = 'kendall'))

acts.cont.perf <- acts.cont.perf[!is.na(performance)]
								 




