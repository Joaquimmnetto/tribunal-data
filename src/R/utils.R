
create.color.scale <- function(sub.name = 'Relations', plot.names = levels(players$relation.offender)){
	require(RColorBrewer)
	#myColors <- brewer.pal(length(plot.names),"Greys")
	#myColors <- brewer.pal(length(plot.names),"Spectral")
	myColors <- brewer.pal(length(plot.names),"Set2")
	#myColors <- c("#000000","#444444","#888888","#BBBBBB","#999999")
	names(myColors) <- plot.names
	col.scale <- scale_colour_manual(name = sub.name, values = myColors)
}

col.rel.offender <- create.color.scale(sub.name = 'Relations', plot.names = levels(players$relation.offender))


med.t.test <- function(x,not_x){
	print("mean/sd x")
	print(mean(x,na.rm=TRUE))
	print(sd(x,na.rm=TRUE))
	print("mean/sd y")
	print(mean(not_x,na.rm=TRUE))
	print(sd(not_x,na.rm=TRUE))
	t.test(x,not_x)
}

correlation.tests.perf <- function(dt=topics.perf, topic){
	print("Correlation tests for performance")
	print('for ally:')
	x <- with(dt[relation.offender=='ally'], cor.test(performance, get(topic), method = 'kendall'))
	print(append(x$p.value,x$estimate))
	
	print('for enemy:')
	x <- with(dt[relation.offender=='enemy'], cor.test(performance, get(topic), method = 'kendall'))
	print(append(x$p.value,x$estimate))
	
	print('for offender:')
	x <- with(dt[relation.offender=='offender'], cor.test(performance, get(topic), method = 'kendall'))
	print(append(x$p.value,x$estimate))
}
correlation.tests.cont <- function(dt=topics.perf, topic){
	print("Correlation tests for contamination")
	print('for ally:')
	x <- with(dt[relation.offender='ally'], cor.test(contamination, get(topic), method = 'kendall'))
	print(append(x$p.value,x$estimate))
	
	print('for enemy:')
	x <- with(dt[relation.offender='enemy'], cor.test(contamination, get(topic), method = 'kendall'))
	print(append(x$p.value,x$estimate))
	
}
correlation.tests <- function(dt=topics.perf, topic){
	correlation.tests.perf(dt,topic)
	correlation.tests.cont(dt,topic)
}


#Remove outliers de um array. Outliers são consireados pontos que estão fora de (med+1.5*iqr, med-1.5*iqr)
#dt - Tabela contendo a coluna
#col__ - string com o nome da coluna da qual vão ser removidos os outliers
#Retorna um data.table contendo somente a coluna selecionada, sem os outliers.
remove.outliers <- function(dt,col_name){
	#col_name <- deparse(substitute(col__))
	summ <- summary(as.matrix(dt[,get(col_name)])[,1])
	iqr = summ[5] - summ[2]
	upper_thresh = summ[5] + 1.5*iqr
	lower_thresh = summ[2] - 1.5*iqr
	ret <- dt[get(col_name) <= upper_thresh & get(col_name) >= lower_thresh]
	return(ret)
} 

#Aplica kmeans + uso dos centroids como pontos nos pontos 2d listados.
#dt - data.table contendo as duas dimensões x e y
#group_size - tamaho das aglomerações que serão feitas.
#x - coluna representando os valores x do ponto 2d.
#y - coluna representando os valores y do ponto 2d.
#Retorna um data.table com duas colunas representando os valores x e y dos pontos reduzidos.
kmn.smoother <- function(dt,group_size,x,y){ 
	x_name <- deparse(substitute(x))
	y_name <- deparse(substitute(y))
	num_groups <- as.integer(nrow(dt)/group_size) + 1
	
	points <- dt[,.(get(x_name),get(y_name))] 
	setnames(points, names(points),c(x_name,y_name))
	kmn <-  points %>% kmeans(centers=num_groups)
	
	points$cl <- kmn$cluster
	
	points <- points[ ,c(x_name,y_name) := .(median(get(x_name)),median(get(y_name))),by=cl ]
	points <- unique(points)
	return(points)
}
#Converte um objeto python salvo em arquivo utilizando o pickle para uma estrutura R.
#pkl_fn - Nome do arquivo salvo utilizando o pickle
pkl2R <- function(pkl_fn){
	library(rPython)
	python.exec("import pickle")
	python.exec(paste("obj = pickle.load(open(",pkl_fn,",'rb'))"))
	return(python.get('obj'))
}

#plot many ggplot graphics in a single image
multiplot <- function(..., plotlist=NULL, file, cols=2, layout=NULL) {
	library(grid)
	
	# Make a list from the ... arguments and plotlist
	plots <- c(list(...), plotlist)
	
	numPlots = length(plots)
	
	# If layout is NULL, then use 'cols' to determine layout
	if (is.null(layout)) {
		# Make the panel
		# ncol: Number of columns of plots
		# nrow: Number of rows needed, calculated from # of cols
		layout <- matrix(seq(1, cols * ceiling(numPlots/cols)),
										 ncol = cols, nrow = ceiling(numPlots/cols))
	}
	
	if (numPlots==1) {
		print(plots[[1]])
		
	} else {
		# Set up the page
		grid.newpage()
		pushViewport(viewport(layout = grid.layout(nrow(layout), ncol(layout))))
		
		# Make each plot, in the correct location
		for (i in 1:numPlots) {
			# Get the i,j matrix positions of the regions that contain this subplot
			matchidx <- as.data.frame(which(layout == i, arr.ind = TRUE))
			
			print(plots[[i]], vp = viewport(layout.pos.row = matchidx$row,
																			layout.pos.col = matchidx$col))
		}
	}
}

plot.something <- function(dt, xcol='value', ycol) {
	plt <- ggplot(data=dt,
								aes(x=get(xcol), y=get(ycol)*100, shape=relation.offender)) + 
		geom_point(alpha=0.3) + 
		geom_smooth(aes(x=get(xcol), color=relation.offender), span=1.0)
	return(plt)
}

add.theme <- function(plt, col.scale=col.rel.offender){
	return(plt + 
			 	theme_bw(base_size=18) + 
				 	theme(plot.margin=unit(c(3,0,0,0),"mm"), legend.key = element_rect(colour = "gray", fill = NA)) +
				 	guides(color=guide_legend(override.aes=list(fill=NA))) +
			 	col.scale
			 )
}
# theme(plot.margin=unit(c(0,0,0,0),"mm")) 

save.plot <- function(fname, plt,w=5,h=5){
	ggsave(fname, plot=plt, device='png', width = w, height = h)
}

mend.plots <- function(plot.a, plot.b, img.fname = 'plot.png', file = FALSE ){
	require(grid)
	if(file){
		png(filename=img.fname, width = 1100, height = 500, units='px', pointsize = 12); 
	}
	grid.newpage()
	pushViewport(viewport(layout = grid.layout(nrow=1,ncol=2,widths=c(1,1.15))))
	print(plot.a, vp = viewport(layout.pos.row=1, layout.pos.col=1))
	print(plot.b, vp = viewport(layout.pos.row=1, layout.pos.col=2))
	if(file){
		dev.off()
	}
}

