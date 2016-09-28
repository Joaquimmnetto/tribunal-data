import csv

csvIn  = open("agr_in.csv",'rb')
csvOut = open("agr_out.csv",'wb')

csvRd = csv.reader(csvIn)
csvWr = csv.writer(csvOut)


prev_match = '0'
match_dict = {}


def write_dict(case,match,match_dict):
	for team in match_dict.keys():
		match_chats = [ [ case,match,team ]+[ champ,' '.join(match_dict[team][champ]) ] for champ in match_dict[team].keys() ]
		csvWr.writerows(match_chats)


for row in csvRd:

	case = row[0]
	match = row[1]
	team = row[2]
	champ = row[3]
	chat = row[4] + " "

	if prev_match != match:
		write_dict(case,match,match_dict.copy())
		match_dict.clear()
		prev_match = match

	if team not in match_dict.keys():
		match_dict[team] = {}

	if champ not in match_dict[team].keys():
		match_dict[team][champ] = []

	match_dict[team][champ].append(chat)

write_dict(case,match,match_dict)
