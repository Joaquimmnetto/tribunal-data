require(dplyr)
require(data.table)
#library(multidplyr)

remove.outliers <- function(dt,col__){
  col_name <- deparse(substitute(col__))
  summ <- summary(as.matrix(dt[,col_name])[,1])
  iqr = summ[5] - summ[2]
  upper_thresh = summ[5] + 1.5*iqr
  lower_thresh = summ[2] - 1.5*iqr
  ret <- dt %>% filter_(paste(col_name,'<=',upper_thresh,' & ',col_name,'>=',lower_thresh))
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

save.image("full_data_text.RData")

system.time({
   source("src/R/graphs.R")
})
