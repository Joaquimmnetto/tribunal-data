import csv

csvIn = open("chat.csv",'rb')
csvOut = open("agr_out.csv",'wb')

players_fl = open('players.csv', 'rb')

csvRd = csv.reader(csvIn)
csvWr = csv.writer(csvOut)

match_wr = csv.reader(players_fl)


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

	if team == '':
		print '%s %s'%(case,match)
	champ = row[3]

	if champ=='':
		print '%s %s' % (case, match)

	if len(row) < 5  or chat ==  'NA':
		print row
		chat = ''
	else:
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

print 'sorting...'
import subprocess
subprocess.call(['bash','sort','agr_out.csv','agr_out.csv'])