common.offense.barplot <- ggplot(data = matchs, aes(x = most.common.offense)) +
    geom_bar() +
    xlab("Tipos de ofensas") + ylab("Número de partidas") +
    annotate("text", x = 1, y = 2800, label = "1 partida sem ofensa",
             angle = 90, color = "blue") +
    theme(axis.text.x=element_text(angle = 45, hjust = 1))

reports.by.reason.barplot <- ggplot(data = reports.by.reason) +
    geom_bar(aes(x = most.common.offense, y = total.reports),
             stat = "identity") +
    xlab("Tipos de ofensas") + ylab("Número de denúncias") +
    annotate("text", x = 1, y = 4500, label = "nenhuma denúncia",
             angle = 90, color = "blue") +
    theme(axis.text.x=element_text(angle = 45, hjust = 1))

time.played.hist <- ggplot(data = matchs, aes(x = time.played)) +
    geom_histogram(bins = 100) +
    xlab("Duração da partida") + ylab("Número de partidas") +
    annotate("text", x = 1800, y = 2400,
             label = "Tempo mínimo da partida (20 min)") + 
    geom_line(arrow = arrow(ends = "first", type = "closed"),
              data = data.frame(x = c(2000, 1400), y = c(2250, 1900)),
              aes(x = x, y = y))

outcome.relation.barplot <- ggplot(data = players) +
    geom_bar(aes(x = relation.offender, fill = outcome)) +
    xlab("Associação com ofensor") + ylab("Número de partidas")

#print(common.offense.barplot)
#print(reports.by.reason.barplot)
#print(time.played.hist)
#print(outcome.relation.barplot)
