# encoding=utf8
import codecs
#import unicodecsv as csv
import csv
import os
import traceback

from threading import Semaphore

import sys

from src.python.matches_producer import TarReader
from src.python.matches_producer import ProducersManager

from src.python.consumer import Consumer
from src.python.process_chat import ChatProcessor
from src.python.process_players import PlayerProcessor
from src.python.process_match import MatchProcessor

print(("Arguments:" + str(sys.argv)))

# tars_dir = sys.argv[1]
# dest_dir = sys.argv[2]
# num_producers = int(sys.argv[3])

tars_dir = "../../dataset/sampley_de_guitarra"
dest_dir = "../.."
num_producers = 3

process_chat_csv = True
process_chat_corpus = True
process_players = True
process_matches = True






# chat_atrs = ['date', 'time', 'sent_to', 'champion_name', 'message', 'association_to_offender', 'name_change'],
# ply_atrs = ['level', 'kills', 'deaths', 'assists', 'gold_earned', 'outcome', 'time_played',
#             'association_to_offender', 'champion_name'],
# match_atrs = ['game_mode', 'game_type', 'premade', 'most_common_report_reason', 'allied_report_count',
#               'enemy_report_count', 'case_total_reports', 'time_played']

chat_atrs=["association_to_offender", "champion_name", "time", "message"]
player_atrs=['association_to_offender','champion_name','kills','deaths','assists','gold_earned','outcome']
match_atrs=['premade','most_common_report_reason','allied_report_count','enemy_report_count','case_total_reports','time_played']

def text_consuming(writer,buffer):
	value = buffer.get()
	writer.write(value)
	del value

def csv_consuming(writer,buffer):
	value = buffer.get()
	writer.writerow(value)
	del value[:]


def set_chat_processing(consumers, processors, process_csv=True, process_corpus=True):
	corpus_consumer = None
	chat_consumer = None

	if process_corpus:
		corpus_fl = codecs.open(dest_dir+'/'+'chat_corpus.txt', 'a',encoding='utf-8')
		corpus_consumer = Consumer(corpus_fl,text_consuming)
		consumers.append(corpus_consumer)

	if process_csv:
		chat_fl = codecs.open(dest_dir+'/'+'chat.csv', "a",encoding='utf-8')
		chat_wr = csv.writer(chat_fl)
		chat_consumer = Consumer(chat_wr,csv_consuming)
		consumers.append(chat_consumer)

	if process_csv or process_corpus:
		processors.append(ChatProcessor(chat_atrs, chat_consumer, corpus_consumer, corpus=process_corpus, csv=process_csv))

def set_players_processing(consumers, processors):
	players_fl = codecs.open(dest_dir+'/'+'players.csv','a',encoding='utf-8')
	players_wr = csv.writer(players_fl)
	player_consumer = Consumer(players_wr,csv_consuming)

	consumers.append(player_consumer)
	processors.append(PlayerProcessor(player_atrs, player_consumer))


def set_matches_processing(consumers, processors):
	matches_fl = codecs.open(dest_dir+'/'+'matches.csv','a',encoding='utf-8')
	matches_wr = csv.writer(matches_fl)
	match_consumer = Consumer(matches_wr,csv_consuming)

	consumers.append(match_consumer)
	processors.append(MatchProcessor(match_atrs, match_consumer))




#---------------------Main-----------------

last_thread = None
consumers = []
processors = []
prod_sem = Semaphore(num_producers)

if process_chat_csv or process_chat_corpus:
	set_chat_processing(consumers, processors, process_chat_csv, process_chat_corpus)

if process_players:
	set_players_processing(consumers, processors)

if process_matches:
	set_matches_processing(consumers, processors)


for consumer in consumers:
	consumer.start()

for tar_name in os.listdir(tars_dir):
	if not (tar_name.endswith('.tar.gz') and 'jsons' in tar_name):
		continue
	try:
		print("Extracting " + str(tar_name))
		tmp_dir = TarReader().extract(tars_dir + "/" + tar_name)

		prod_sem.acquire()
		print("Processing " + str(tar_name))
		last_thread = ProducersManager(tmp_dir, processors, prod_sem).start()
	except:
		traceback.print_exc()


last_thread.join() if last_thread is not None else None


for consumer in consumers:
	consumer.stop()

for consumer in consumers:
	consumer.join()

print('Organizando resultados...')
import subprocess
subprocess.call(['bash','sort','chat.csv','chat.csv'])
subprocess.call(['bash','sort','players.csv','players.csv'])
subprocess.call(['bash','sort','matches.csv','matches.csv'])








