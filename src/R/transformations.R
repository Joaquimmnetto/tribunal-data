require(dplyr)
#library(multidplyr)

#range01 <- function(x){(x-min(x))/(max(x)-min(x))}
system.time({
source("src/R/preprocessing.R")
})
system.time({
source("src/R/performance.R")
})
system.time({
source("src/R/contamination.R")
})