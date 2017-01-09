#---------A presença de uma justificativa textual na denúncia está associada com um grau maior de toxicidade?

'full-wout'
summary(matches[report.text.allies=='' & report.text.enemies=='']$match.contamination)
'full-with'
summary(matches[report.text.allies!='' | report.text.enemies!='']$match.contamination)
'full-full'
summary(matches$match.contamination)

"enemies-wout"
summary(matches[report.text.enemies=='']$enemy.contamination)
"enemies-with"
summary(matches[report.text.enemies!='']$enemy.contamination)
"enemies-full"
summary(matches$enemy.contamination)

"allies-wout"
summary(matches[report.text.allies=='']$ally.contamination)
"allies-with"
summary(matches[report.text.allies!='']$ally.contamination)
"allies-full"
summary(matches$ally.contamination)


nrow(matches[report.text.allies==''&report.text.enemies==''])/nrow(matches)

p <- ggplot() + 
        geom_boxplot(data=matches,aes(x="match-full",y=match.contamination)) +
          geom_boxplot(data=matches[report.text.allies=='' & report.text.enemies==''],aes(x="match-wout",y=match.contamination)) +
          geom_boxplot(data=matches[report.text.allies!='' | report.text.enemies!=''],aes(x="match-with",y=match.contamination)) +
        geom_boxplot(data=matches,aes(x="ally-full",y=ally.contamination),color='blue') +
          geom_boxplot(data=matches[report.text.allies==''],aes(x="ally-wout",y=ally.contamination),color='blue') +
          geom_boxplot(data=matches[report.text.allies!=''],aes(x="ally-with",y=ally.contamination),color='blue') +
        geom_boxplot(data=matches,aes(x="enemy-full",y=enemy.contamination),color='red') +
          geom_boxplot(data=matches[report.text.enemies==''],aes(x="enemy-wout",y=enemy.contamination),color='red') +
          geom_boxplot(data=matches[report.text.enemies!=''],aes(x="enemy-with",y=enemy.contamination),color='red')

nrow(matches[report.text.allies!=''])/nrow(matches)