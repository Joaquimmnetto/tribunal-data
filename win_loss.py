import csv

agr_fl = open("agr_out.csv")
players_fl = open("players.csv")

agr_rd = csv.reader(agr_fl)
players_rd = csv.reader(players_fl)




for row_agr,row_ply in agr_rd,players_rd:

	row_ply += row_agr[5]











