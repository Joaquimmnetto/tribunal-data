setwd('~/PyCharm-Workspace/tribunaldb/')
require(dplyr)
library(dtplyr)
require(data.table)
source('src/R/utils.R')


players_fl = "data/full/players.csv"
matches_fl = "data/full/matches.csv"
system.time({
  players <- setDT(fread(players_fl, header = FALSE, sep=',', showProgress=TRUE,
                         col.names = c("case", "match", "relation.offender", "champion", 
                                       "kills", "deaths","assists", "gold", "outcome"),
                         colClasses = c("factor", "factor", "factor", "factor",
                                        "integer", "integer", "integer","integer", "factor")))
  
  matches <- setDT(fread(matches_fl, header = FALSE, sep=',', showProgress=TRUE, 
                         col.names = c("case", "match", "match.type", "most.common.offense",
                                       'report.text.allies', 'report.text.enemies',
                                       "reports.allies", "reports.enemies", "time.played"), 
                         colClasses = c("factor", "factor", "factor", "factor",
                                        "character","character",
                                        "integer", "integer", "integer")))
   setkey(matches,case,match)
  setkey(players,case,match,relation.offender)
  
    
})
system.time({
source("src/R/performance.R")
})
system.time({
source("src/R/contamination.R")
})
system.time({
#source("src/R/groups.R")
})
