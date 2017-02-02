require(dplyr)
library(dtplyr)
require(data.table)
#library(multidplyr)

remove.outliers <- function(dt,col__){
  col_name <- deparse(substitute(col__))
  summ <- summary(as.matrix(dt[,col_name])[,1])
  iqr = summ[5] - summ[2]
  upper_thresh = summ[5] + 1.5*iqr
  lower_thresh = summ[2] - 1.5*iqr
  ret <- dt[get(col_name) <= upper_thresh & get(col_name) >= lower_thresh]
  return(ret)
} 


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

pkl2R <- function(pkl_fn){
  library(rPython)
  python.exec("import pickle")
  python.exec(paste("obj = pickle.load(open(",pkl_fn,",'rb'))"))
  return(python.get('obj'))
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

system.time({
source("src/R/groups.R")
})
