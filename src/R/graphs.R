common.offense.barplot <- ggplot(data = matches, aes(x = most.common.offense)) +
    geom_bar() +
    xlab("Tipos de ofensas") + ylab("Número de partidas") +
    annotate("text", x = 1, y = 3200, label = "1 partida sem ofensa",
             angle = 90, color = "red") +
    theme(axis.text.x=element_text(angle = 45, hjust = 1))

reports.by.reason.barplot <- ggplot(data = reports.by.reason) +
    geom_bar(aes(x = most.common.offense, y = total.reports),
             stat = "identity") +
    xlab("Tipos de ofensas") + ylab("Número de denúncias") +
    annotate("text", x = 1, y = 5400, label = "nenhuma denúncia",
             angle = 90, color = "red") +
    theme(axis.text.x=element_text(angle = 45, hjust = 1))

time.played.hist <- ggplot(data = matches, aes(x = time.played)) +
    geom_histogram(bins = 100) +
    xlab("Duração da partida (segundos)") + ylab("Número de partidas") +
    annotate("text", x = 1800, y = 2400, color = "red",
             label = "Tempo mínimo de permanência (20 min)") + 
    geom_line(arrow = arrow(ends = "first", type = "closed"),
              data = data.frame(x = c(2000, 1400), y = c(2250, 1900)),
              aes(x = x, y = y), color = "red")

outcome.relation.barplot <- ggplot(data = players) +
    geom_bar(aes(x = relation.offender, fill = outcome)) +
    xlab("Associação com ofensor") + ylab("Número de partidas")

allies.win.time.played.hist <- ggplot(data = allies.win) +
                               geom_histogram(aes(x = time.played), bins = 100) +
                               geom_vline(xintercept = mean(allies.win$time.played), color = "red") +
                               xlim(0, 5000) + 
                               xlab("Duração da partida (segundos)") +
                               ylab("Número de partidas") +
                               ggtitle("Vitória dos aliados") +
                               annotate("text", x = 3000, y = 1700,
                                        color = "red", label = "Média = 2075.5 segundos")

enemies.win.time.played.hist <- ggplot(data = enemies.win) +
                                geom_histogram(aes(x = time.played), bins = 100) +
                                geom_vline(xintercept = mean(enemies.win$time.played), color = "red") +
                                xlim(0, 5000) +
                                xlab("Duração da partida (segundos)") +
                                ylab("Número de partidas") +
                                ggtitle("Vitória dos adversários") +
                                        annotate("text", x = 2900, y = 7800,
                                        color = "red", label = "Média = 1938.2 segundos")

allies.gold.hist <- ggplot(data = allies) +
                    geom_histogram(aes(x = gold), bins = 100) +
                    geom_vline(xintercept = mean(allies$gold), color = "red") +
                    xlim(0, 20500) +
                    xlab("Recompensa (ouro)") +
                    ylab("Número de partidas") +
                    ggtitle("Recompensa dos aliados") +
                    annotate("text", x = 12500, y = 3100, color = "red",
                             label = "Média = 8927.2 (ouro)")

enemies.gold.hist <- ggplot(data = enemies) +
                         geom_histogram(aes(x = gold), bins = 100) +
                         geom_vline(xintercept = mean(enemies$gold), color = "red") +
                         xlim(0, 20500) +
                         xlab("Recompensa (ouro)") +
                         ylab("Número de partidas") +
                         ggtitle("Recompensa dos adversários") +
                         annotate("text", x = 13700, y = 3780, color = "red",
                                  label = "Média = 10166 (ouro)")
