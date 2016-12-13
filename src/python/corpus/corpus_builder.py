# encoding=utf8

import os
import sys
#import codecs
import csv

import traceback
from threading import Semaphore

from classes.consumer import Consumer
from classes.matches_producer import ProducersManager
from classes.matches_producer import TarReader
from classes.process_chat import ChatProcessor
from classes.process_players import PlayerProcessor

from classes.process_match import MatchProcessor

print(("Arguments:" + str(sys.argv)))

tars_dir = "../../../sampley_de_guitarra" if len(sys.argv) < 2 else sys.argv[1]
dest_dir = "../../.." if len(sys.argv) < 3 else sys.argv[2]
num_producers = 10 if len(sys.argv) < 4 else int(sys.argv[3])

chat_csv_name = 'chat.csv' if len(sys.argv) < 5 else str(sys.argv[4])
chat_corpus_name = 'corpus.txt' if len(sys.argv) < 6  else str(sys.argv[5])
players_name = 'players.csv' if len(sys.argv) < 7  else str(sys.argv[6])
matches_name = 'matches.csv' if len(sys.argv) < 8 else str(sys.argv[7])

# chat_atrs = ['date', 'time', 'sent_to', 'champion_name', 'message', 'association_to_offender', 'name_change'],
# ply_atrs = ['level', 'kills', 'deaths', 'assists', 'gold_earned', 'outcome', 'time_played',
#             'association_to_offender', 'champion_name'],
# match_atrs = ['game_mode', 'game_type', 'premade', 'most_common_report_reason', 'allied_report_count',
#               'enemy_report_count', 'case_total_reports', 'time_played']

chat_atrs = ["association_to_offender", "champion_name", "time", "message"]
player_atrs = ['association_to_offender', 'champion_name', 'kills', 'deaths', 'assists', 'gold_earned', 'outcome']
match_atrs = ['game_type', 'most_common_report_reason','allied_report_count', 'enemy_report_count', 'time_played']


def text_consuming(writer, value):
	writer.write(value)
	del value


def csv_consuming(writer, value):
	writer.writerow(value)
	del value[:]


def set_chat_processing(consumers, processors, process_csv=True, process_corpus=True):
	corpus_consumer = None
	chat_consumer = None

	if process_corpus:
		corpus_fl = open(dest_dir + '/' + chat_corpus_name, 'at', encoding='utf-8')
		corpus_consumer = Consumer(corpus_fl, text_consuming)
		consumers.append(corpus_consumer)

	if process_csv:
		chat_fl = open(dest_dir + '/' + chat_csv_name, "at", encoding='utf-8')
		chat_wr = csv.writer(chat_fl)
		chat_consumer = Consumer(chat_wr, csv_consuming)
		consumers.append(chat_consumer)

	if process_csv or process_corpus:
		processors.append(ChatProcessor(chat_atrs, chat_consumer, corpus_consumer,
		                                corpus=process_corpus, csv=process_csv,
		                                filters=[]))


def set_players_processing(consumers, processors):
	players_fl = open(dest_dir + '/' + players_name, 'at', encoding='utf-8')
	players_wr = csv.writer(players_fl)
	player_consumer = Consumer(players_wr, csv_consuming)

	consumers.append(player_consumer)
	processors.append( PlayerProcessor(player_atrs, player_consumer, []) )


def set_matches_processing(consumers, processors):
	matches_fl = open(dest_dir + '/' + matches_name, 'at', encoding='utf-8')
	matches_wr = csv.writer(matches_fl)
	match_consumer = Consumer(matches_wr, csv_consuming)

	consumers.append(match_consumer)
	processors.append(MatchProcessor(match_atrs, match_consumer))


# ---------------------Main-----------------

consumers = []
processors = []
prod_sem = Semaphore(num_producers)

if chat_csv_name != "None" or chat_corpus_name != "None":
	set_chat_processing( consumers, processors, chat_csv_name != "None", chat_corpus_name != "None" )

if players_name != "None":
	set_players_processing(consumers, processors)

if matches_name != "None":
	set_matches_processing(consumers, processors)

for consumer in consumers:
	consumer.start()

producers = []
for tar_name in os.listdir(tars_dir):
	if not (tar_name.endswith('.tar.gz') and 'jsons' in tar_name):
		continue
	try:
		prod_sem.acquire()
		t = ProducersManager(tars_dir + "/" + tar_name, processors, prod_sem)
		producers.append(t)
		t.start()
	except:
		traceback.print_exc()


print('Esperando produtores...')
for producer in producers:
	if producer.is_alive():
		producer.join()

print('Parando consumidores...')
for consumer in consumers:
	consumer.stop()

print("Esperando pelos consumidores...")
for consumer in consumers:
	consumer.join(timeout=10)

print('Finalizado!')

#import subprocess
#import platform

# if platform.system() == "Windows":
# 	subprocess.call(['bash', 'sort.sh', 'chat.csv', 'chat.csv'])
# 	subprocess.call(['bash', 'sort.sh', 'players.csv', 'players.csv'])
# 	subprocess.call(['bash', 'sort.sh', 'matches.csv', 'matches.csv'])
# else:
# 	subprocess.call(['sort.sh', 'chat.csv', 'chat.csv'])
# 	subprocess.call(['sort.sh', 'players.csv', 'players.csv'])
# 	subprocess.call(['sort.sh', 'matches.csv', 'matches.csv'])
