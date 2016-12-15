require(dplyr)
require(data.table)
#library(multidplyr)

system.time({
source("src/R/preprocessing.R")
})
system.time({
source("src/R/performance.R")
})
system.time({
source("src/R/contamination.R")
})
save.image("full_data.RData")
