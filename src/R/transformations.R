require(dplyr)
require(data.table)
#library(multidplyr)

#range01 <- function(x){(x-min(x))/(max(x)-min(x))}
system.time({
source("src/R/preprocessing.R")
})
#Salvando dados agora pré-processados.
#save.image("preprocessed.RData")
system.time({
source("src/R/performance.R")
})
#save.image("performance.RData")
system.time({
source("src/R/contamination.R")
})
#save.image("full_data.RData")