import csv
import json
import tarfile
import os
import shutil
import thread
import random
import string
import traceback
import datetime



from Queue import Queue
from threading import Semaphore
from threading import Thread

finished = False
numProducers = 1
consumers = []

import sys
print sys.argv
tardir = sys.argv[1]

prodSem = Semaphore(numProducers)

#folder = '../../dataset'
folder = tardir

corpus_fl = open(sys.argv[2], 'ab')

chat_fl = open('../../chat.csv', "ab")
chat_wr = csv.writer(chat_fl)

players_fl = open('../../players.csv','ab')
players_wr = csv.writer(players_fl)

matches_fl = open('../../matches.csv','ab')
matches_wr = csv.writer(matches_fl)

chat_buffer = None
players_buffer = None
matches_buffer = None
corpus_buffer = None

TIME_WINDOW = 5

def corpus_chat(case):
	corpus_lst = list()
	players_buffer = {}
	players_t0 = {}
	for match_num,match in enumerate(case):
		for entry in match['chat_log']:
			player = (entry['association_to_offender'],entry['champion_name'])
			timestamp = datetime.strptime(entry['time'],"%H:%M:%S").total_seconds()

			if not player in players_t0.keys():
				players_t0[player] = timestamp

			if timestamp - players_t0[player] > TIME_WINDOW:
				corpus_lst.append(players_buffer[player].encode("utf-8"))
				players_buffer[player] = ""
				players_t0[player] = timestamp

			if not player in players_buffer.keys():
				players_buffer[player] = ""

			players_buffer[player] += entry['message'] + " "





	return ' '.join(corpus_lst)


# def put_NA(match_players):
# 	for row in match_players:
# 		for i,value in enumerate(row):
# 			if row[i] is None or str(row[i]).strip() == '':
# 				row[i] = 'NA'
#
# 	return match_players





def process_csv(case, chat_atrs = None, ply_atrs = None, match_atrs = None):

	if chat_atrs == None:
		chat_atrs = ['date', 'time', 'sent_to', 'champion_name', 'message', 'association_to_offender', 'name_change']

	if ply_atrs == None:
		ply_atrs = ['level','kills','deaths','assists','gold_earned','outcome','time_played','association_to_offender',
		            'champion_name']

	if match_atrs == None:
		match_atrs = ['game_mode','game_type','premade','most_common_report_reason','allied_report_count',
		              'enemy_report_count','case_total_reports','time_played']

	case_chat = []
	case_players = []
	case_matches = []
	for match_num,match in enumerate(case):
		if len(chat_atrs) > 0:
			match_chat = process_chat(match_num, match, chat_atrs)
			if match_chat is None:
				pass
			case_chat += match_chat

		if len(ply_atrs) > 0:
			match_players = process_players(match_num,match,ply_atrs)
			case_players += match_players

		if len(match_atrs) > 0:
			match_info = process_info(match_num,match, match_atrs)
			case_matches += match_info

	return case_chat,case_players,case_matches


def process_chat(match_num,match,atrs):
	case_id = match['case_id']
	match_chat = []
	for entry in match['chat_log']:
		csv_array = list()
		csv_array.append(case_id)
		csv_array.append(match_num)
		for attr in atrs:
			if attr == 'message':
				if not any(entry[attr]):
					csv_array.append("")
				else:
					csv_array.append(entry[attr].encode('utf-8'))
			else:
				csv_array.append(entry[attr])
		match_chat.append(csv_array)

	return match_chat


def process_players(match_num,match,atrs):
	case_id = match['case_id']
	match_players = []
	for entry in match['players']:
		csv_array = list()
		csv_array.append(case_id)
		csv_array.append(match_num)
		for atr in atrs:
			value = None
			if atr == 'kills' or atr == 'deaths' or atr == 'assists':
				value = entry['scores'][atr]
			else:
				value = entry[atr]
			csv_array.append(value)

		match_players.append(csv_array)

	return match_players

# def fix_relation_offender(atrs, players_arrays):
# 	ally_outcome = None
# 	enemy_outcome = None
# 	offender_count = 0
#
# 	for entry in players_arrays:
# 		relation_offender = entry[atrs.index("association_to_offender")+2].strip().lower()
# 		outcome = entry[atrs.index("outcome")+2]
#
# 		if relation_offender == 'ally':
# 			ally_outcome = outcome
# 		elif relation_offender =='enemy':
# 			enemy_outcome = outcome
# 		elif relation_offender == 'offender':
# 			offender_count+=1
#
# 	for entry in players_arrays:
# 		relation_offender = entry[atrs.index("association_to_offender")+2].strip().lower()
# 		outcome = entry[atrs.index("outcome")+2]
#
# 		if not relation_offender:
# 			if (not ally_outcome is None) and outcome==ally_outcome:
# 				if offender_count == 0:
# 					relation_offender = 'offender'
# 				else:
# 					relation_offender = 'ally'
# 			elif (not enemy_outcome is None) and outcome==enemy_outcome:
# 				relation_offender = 'enemy'
#
# 			entry[atrs.index("association_to_offender")] = relation_offender
# 			return len(relation_offender) > 0
#
#
# 	return True







def process_info(match_num, match, atrs):
	case_id = match['case_id']
	match_players = []
	csv_array = list()
	csv_array.append(case_id)
	csv_array.append(match_num)
	for atr in atrs:
		if atr == 'time_played':
			value = match['players'][0]['time_played']
		else:
			value = match[atr]
		csv_array.append(value)
	match_players.append(csv_array)

	return match_players



def process_jsons(jsonsFile):
	case = []
	case_id = os.path.basename(jsonsFile.name).split('.')[0]
	for match_num, json_str in enumerate(jsonsFile):
		try:
			if json_str.strip().strip('\n').strip('"') == '':
				continue
			match = json.loads(json_str)

			match['case_id'] = case_id
			case.append(match)

		except:
			print 'erro no json'


	return case


def process_tar(tarName, tmp_dir):
	try:
		os.mkdir(tmp_dir)

		game_tar = tarfile.open(folder + '/' + tarName, 'r:gz')
		game_tar.extractall(tmp_dir)

		game_tar.close()

		for jsonsname in os.listdir(tmp_dir):
			jsonsFile = open(tmp_dir + '/' + jsonsname, 'rb')
			jsons = process_jsons(jsonsFile)

			chat_data,players_data,match_data = process_csv(jsons,
										    chat_atrs=["association_to_offender", "champion_name", "message"],
										    ply_atrs=['association_to_offender','champion_name','kills','deaths','assists','gold_earned','outcome'],
			                               match_atrs=['premade','most_common_report_reason','allied_report_count',
			                                            'enemy_report_count','case_total_reports','time_played'])
			corpus_data = corpus_chat(jsons)

			feed_consumer(chat_buffer,chat_data)
			feed_consumer(corpus_buffer,corpus_data)
			feed_consumer(players_buffer,players_data)
			feed_consumer(matches_buffer,match_data)

			jsonsFile.close()


		print 'Fechando '+tarName +' sem erros...'
	except Exception as e:
		print 'Erro em ',tarName
		traceback.print_exc()
	finally:
		shutil.rmtree(tmp_dir)
		prodSem.release()


def feed_consumer(consumer_buffer,data):
	if consumer_buffer is not None and len(data) > 0:
		consumer_buffer.put(data)


def create_csv_consumer(csv_wr,matrix_buffer):

	def consumer(_csv_wr, _matrix_buffer):
		try:
			while True:
				if finished:
					matrix = _matrix_buffer.get(timeout=10)
				else:
					matrix = _matrix_buffer.get(timeout=60)
				_csv_wr.writerows(matrix)
				del matrix
		except:
			traceback.print_exc()
			print 'consumer finished'


	t = Thread(None,consumer,None,(csv_wr, matrix_buffer))
	consumers.append(t)
	t.start()


def create_text_consumer(txt_file,txt_buffer):

	def consumer(_txt_file, _txt_buffer):
		try:
			while True:
				if finished:
					corpus = _txt_buffer.get(timeout=10)
				else:
					corpus = _txt_buffer.get(timeout=60)

				_txt_file.write(corpus)
				del corpus
		except:
			traceback.print_exc()
			print 'consumer finished'


	t = Thread(None,consumer,None,(txt_file,txt_buffer))
	consumers.append(t)
	t.start()


#---------------------Main-----------------

chat_buffer = Queue()
create_csv_consumer(chat_wr, chat_buffer)
players_buffer = Queue()
create_csv_consumer(players_wr,players_buffer)
matches_buffer = Queue()
create_csv_consumer(matches_wr,matches_buffer)
corpus_buffer = Queue()
create_text_consumer(corpus_fl, corpus_buffer)


dirs = []
for tarName in os.listdir(folder):
	if not (tarName.endswith('.tar.gz') and 'jsons' in tarName):
		continue
	prodSem.acquire()
	print "Processing " + tarName
	tmpDir = ''.join(random.choice(string.lowercase) for i in range(5))
	t = Thread(None,process_tar,None,(tarName,tmpDir))
	t.start()

	dirs.append(tmpDir)

t.join()
finished = True


for consumer in consumers:
	consumer.join()

# for dir in dirs:
# 	shutil.rmtree(dir)

chat_fl.close()
players_fl.close()
corpus_fl.close()

print 'Organizando resultados...'
import subprocess
subprocess.call(['bash','sort','chat.csv','chat.csv'])
subprocess.call(['bash','sort','players.csv','players.csv'])
subprocess.call(['bash','sort','matches.csv','matches.csv'])








