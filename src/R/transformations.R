require(dplyr)
require(data.table)
#library(multidplyr)

remove.outliers <- function(dt,col__){
  col_name <- deparse(substitute(col__))
  threshold <- min(boxplot(dt[,c(col_name)])$out)
  ret <- dt %>% filter_(paste(col_name,'<=',threshold))
  return(ret)
}


kmn.smoother <- function(dt,group_size,x,y){ 
  x_name <- deparse(substitute(x))
  y_name <- deparse(substitute(y))
  num_groups = as.integer(nrow(dt)/group_size) + 1
  
  kmn <- dt %>% select_(x_name,y_name) %>% 
    kmeans(centers=num_groups)
  medians <- dt %>% select_(x_name,y_name)
  medians$cl = kmn$cluster
  medians <- medians %>% group_by(cl) 
  medians <- medians %>% summarise_each(funs(median))
  return(medians)
}

system.time({
source("src/R/preprocessing.R")
})
system.time({
source("src/R/performance.R")
})
system.time({
source("src/R/contamination.R")
})
save.image("sample_data.RData")


matches.no.out <- matches %>% remove.outliers(match.contamination) %>% remove.outliers(match.performance)


#plotando com menos densidade
medians <- matches %>% kmn.smoother(100, match.contamination, match.performance)
require(ggplot2)
ggplot(medians) + geom_point(aes(x=match.contamination,y=match.performance)) + 
                                  geom_smooth(aes(x=match.contamination,y=match.performance))
