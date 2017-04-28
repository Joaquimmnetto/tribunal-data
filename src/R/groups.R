require(data.table)
require(rPython)
source('src/R/utils.R')


rel.ofndr <- "full"
topics <- pkl2R(paste("'data/",rel.ofndr,"/lda_labels_10.pkl'", sep=''))
r2d <- pkl2R(paste("'data/",rel.ofndr,"/cnt_team_r2d.pkl'", sep=''))
	
topics <- cbind(data.table(t(matrix(unlist(r2d), nrow=length(unlist(r2d[1]))))),as.data.table(topics))
rm(r2d)
names(topics) <- c("case", "match", "relation.offender", "topics")
setkey(topics, case, match)

{ #Insert topics columns in matches

	matches <- merge(matches,
								 topics[relation.offender == 'ally'
											][,ally.topics := factor(topics)
											][,c('relation.offender','topics') := NULL]
								 , all.x=TRUE)
	matches <- merge(matches,
										 topics[relation.offender == 'enemy'
										 			 ][,enemy.topics := factor(topics)
										 			 	][,c('relation.offender','topics') := NULL]
										 , all.x=TRUE)
	matches <- merge(matches,
									 topics[relation.offender == 'offender'
									 			 ][,offender.topics := factor(topics)
									 			 	][,c('relation.offender','topics') := NULL]
									 , all.x=TRUE)
	rm(topics)
		
	matches <- matches[,ally.topics := factor(
						ifelse(ally.topics==0 | ally.topics==9,
							 				 							"tactics",
						 ifelse(ally.topics==2 | ally.topics==3,
							 			 								"complaints",
						 ifelse(ally.topics==4, "arguments",
						 ifelse(ally.topics==5, "tactics.pos",
						 ifelse(ally.topics==6, "chit.chat",						 			 
						 ifelse(ally.topics==7, "insults",						 			 
						 ifelse(ally.topics==8, "taunts",						 			 
						 ifelse(ally.topics==1, "other.langs",
						 			 									NA)))))))))
						]
	matches <- matches[,enemy.topics := factor(
		ifelse(enemy.topics==0 | enemy.topics==9,
					 													"tactics",
					 	ifelse(enemy.topics==2 | enemy.topics==3,
					 			 										"complaints",
		 			 	ifelse(enemy.topics==4, "arguments",
					 	ifelse(enemy.topics==5, "tactics.pos",
						ifelse(enemy.topics==6, "chit.chat",						 			 
						ifelse(enemy.topics==7, "insults",						 			 
						ifelse(enemy.topics==8, "taunts",						 			 
						ifelse(enemy.topics==1, "other.langs",
																		NA)))))))))
		]
	
	matches <- matches[,offender.topics := factor(
						ifelse(offender.topics==0 | offender.topics==9,
					 													"tactics",
					 	ifelse(offender.topics==2 | offender.topics==3,
					 			 										"complaints",
					 	ifelse(offender.topics==4, "arguments",
					 	ifelse(offender.topics==5, "tactics.pos",
					 	ifelse(offender.topics==6, "chit.chat",						 			 
					 	ifelse(offender.topics==7, "insults",						 			 
					 	ifelse(offender.topics==8, "taunts",						 			 
					 	ifelse(offender.topics==1, "other.langs",
					 													NA)))))))))
	]
}

{ # Create groups table
	ally.groups <- matches[,.(case,match,ally.performance,ally.contamination,ally.groups,report.text.allies)][,relation.offender := 'ally']
	setnames(ally.groups, old = c('ally.performance','ally.contamination', 'ally.groups', 'report.text.allies'), new = c('performance','contamination', 'topic', 'report.text'))
	enemy.groups <- matches[,.(case,match,enemy.performance,enemy.contamination,enemy.groups,report.text.enemies)][,relation.offender := 'enemy']
	setnames(enemy.groups, old = c('enemy.performance','enemy.contamination', 'enemy.groups', 'report.text.enemies'), new = c('performance','contamination', 'topic', 'report.text'))
	offender.groups <- matches[,.(case,match,offender.performance,NA,offender.groups,NA)][,relation.offender := 'offender']
	setnames(offender.groups, old = c('offender.performance','V4', 'offender.groups', 'V6'), new = c('performance','contamination', 'topic', 'report.text'))
	
	groups <- rbind(ally.groups,enemy.groups,offender.groups)
	rm('ally.groups','enemy.groups','offender.groups')
	
	groups <- groups[,topic.2 := factor(ifelse(topic == 'chit.chat' | topic == 'tactics' | topic == 'tactics.pos','pos',
																			ifelse(topic =='arguments' | topic =='complaints' | topic =='insults' | topic =='taunts','neg',NA)))]
}

build.topics.aggr <- function(dt = matches, value.col, topics.col, col.name = 'value', agr.size = 10000){
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
																"chit.chat" = prop.table(summary(topics))['chit.chat'],
																"taunts" = prop.table(summary(topics))['taunts'],
																"tactics" = prop.table(summary(topics))['tactics'],
																"tactics.pos" = prop.table(summary(topics))['tactics.pos'],
																"other.langs" = prop.table(summary(topics))['other.langs'],
																"nas" = prop.table(summary(topics))["NA's"]
															),by=i]
	
	colnames(topics.aggr)[2] = col.name
	
	topics.aggr <- topics.aggr[, tactics.full := tactics + tactics.pos]
	topics.aggr <- topics.aggr[, mood := tactics.pos + chit.chat]
	topics.aggr <- topics.aggr[, insults.prov := insults + taunts]
	
	topics.aggr <- topics.aggr[, neg := arguments + complaints + insults + taunts]
	topics.aggr <- topics.aggr[, neg := complaints + insults + taunts]
	topics.aggr <- topics.aggr[, pos := chit.chat + tactics.full]
	
	return(topics.aggr)
}

ally.topics.cont <- build.topics.aggr('ally.contamination','ally.topics')
enemy.topics.cont <- build.topics.aggr('enemy.contamination','enemy.topics')
ally.topics.cont <- ally.topics.cont[,relation.offender := 'ally']
enemy.topics.cont <- enemy.topics.cont[,relation.offender := 'enemy']
topics.cont <- rbind(ally.topics.cont,enemy.topics.cont)

ec.topics.cont <- build.topics.aggr(matches[enemy.contamination>0],'enemy.contamination','enemy.topics')

offender.ally.topics.cont <- build.topics.aggr('ally.contamination', 'offender.topics')
offender.enemy.topics.cont <- build.topics.aggr('enemy.contamination', 'offender.topics')
offender.ally.topics.cont <- offender.ally.topics.cont[,relation.offender := 'ally']
offender.enemy.topics.cont <- offender.enemy.topics.cont[,relation.offender := 'enemy']
offender.topics.cont <- rbind(offender.ally.topics.cont,offender.enemy.topics.cont)



ally.topics.perf <- build.topics.aggr('ally.performance','ally.topics')
enemy.topics.perf <- build.topics.aggr('enemy.performance','enemy.topics')
offender.topics.perf <- build.topics.aggr('offender.performance','offender.topics')
ally.topics.perf <- ally.topics.perf[,relation.offender := 'ally']
enemy.topics.perf <- enemy.topics.perf[,relation.offender := 'enemy']
offender.topics.perf <- offender.topics.perf[,relation.offender := 'offender']
topics.perf <- rbind(ally.topics.perf, enemy.topics.perf, offender.topics.perf)

offender.ally.topics.perf <- build.topics.aggr('ally.performance','offender.topics')
offender.enemy.topics.perf <- build.topics.aggr('enemy.performance','offender.topics')
cont.topics.perf <- build.topics.aggr(groups[relation.offender!='enemy' | contamination > 0],'performance','topic')
nc.topics.perf <- build.topics.aggr(matches[enemy.contamination==0],'enemy.performance','enemy.topics')
nc.offender.topics.perf <- build.topics.aggr(matches[enemy.contamination==0],'enemy.performance','offender.topics')
ec.topics.perf <- build.topics.aggr(matches[enemy.contamination > 0],'enemy.performance','enemy.topics')




#---------------Plotey stuff-----------------
# 
# require(RColorBrewer)
# myColors <- brewer.pal(3,"Greys")
# names(myColors) <- levels(players$relation.offender)
# col.scale <- scale_colour_manual(name = 'Relations',values = myColors)

med.t.test(
matches[enemy.contamination==0 & (enemy.groups=='tactics' | enemy.groups=='tactics.pos')]$enemy.performance,
matches[enemy.contamination==0 & (enemy.groups!='tactics' & enemy.groups!='tactics.pos')]$enemy.performance)

plot.topic <- function(dt.cont = topics.cont, dt.perf = topics.perf, colname, yname, file = FALSE){
	cont.plot <- add.theme(plot.something(dt.cont,'contamination',colname) +
								labs(x='Group Contamination',y=yname, shape="Aggregations", color='Groups'))
	ggsave(plot=cont.plot, filename=paste(colname,'cont.png',sep='-'), device='png',width = 4,height = 4)
	
	perf.plot <- add.theme(plot.something(dt.perf,'performance',colname) + 
								labs(x='Group Performance',y = element_blank(), shape="Aggregations", color="Groups"))
	ggsave(plot=perf.plot, filename=paste(colname,'perf.png',sep='-'), device='png',width = 4,height = 4)	
	
	fname=paste(colname,'.png',sep='')
	mend.plots(cont.plot, perf.plot, img.fname = fname, file=FALSE)	
}


plot.contaminations <- function(dt=topics.cont, colname1, yname1, colname2, yname2) {
	cont.plot <- add.theme(plot.something(dt, 'contamination', colname1) +
													labs(x='Ally & Enemy Groups Contamination',y=yname1, shape="Aggregations", color='Groups'))
	
	cont.plot2 <- add.theme(plot.something(dt, 'contamination', colname2) +
													labs(x='Ally & Enemy Groups Contamination',y=yname2, shape="Aggregations", color='Groups'))
	
	fname = paste(colname1,'-',colname2,'.png',sep='')
	mend.plots(cont.plot, cont.plot2, img.fname = fname, file = FALSE)
}

plot.topic(colname='pos', yname='Groups w/ Positive Topics (%)')
plot.contaminations(dt = topics.cont, 'complaints', 'Groups w/ Complaints Topic (%)',
										'arguments', 'Groups w/ Arguments Topic (%)')
plot.contaminations(dt = topics.cont, 'insults', 'Groups w/ Insults Topic (%)',
										'taunts', 'Groups w/ Taunts Topic (%)')




labels_offender_groups = factor(offender.topics.cont$relation.offender, labels = 
													c('Offender per Ally', 'Offender per Enemy'))
ggplot(data=offender.topics.cont, 
				 aes(x=contamination, y=complaints * 100, shape=relation.offender)) + 
	geom_point() + geom_smooth(aes(x=jitter(contamination), color=labels_offender_groups)) +
	theme_bw() + col.scale + 
	labs(x='Group Contamination',y="Offender Complaints Topic Groups",
			 shape="Aggregations", color="Relations")
ggsave('offender-complaints-cont.png', device='png', width = 4, height = 4)

x <- get.theme(labs(x='Group Contamination',y="Offender Complaints Topic Groups",
							 shape="Aggregations", color="Relations"))
class(x)
