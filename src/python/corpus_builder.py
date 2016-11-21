# encoding=utf8

import os
import sys
import codecs
import csv
import asyncio

import traceback
from threading import Semaphore

from classes.consumer import Consumer
from classes.matches_producer import ProducersManager
from classes.matches_producer import TarReader
from classes.process_chat import ChatProcessor
from classes.process_players import PlayerProcessor

from classes.process_match import MatchProcessor

print(("Arguments:" + str(sys.argv)))

tars_dir = "../../sampley_de_guitarra" if len(sys.argv) < 2 else sys.argv[1]
dest_dir = "../.." if len(sys.argv) < 3 else sys.argv[2]
num_producers = 3 if len(sys.argv) < 4 else int(sys.argv[3])

chat_csv_name = 'chat.csv' if len(sys.argv) < 5 else str(sys.argv[4])
chat_corpus_name = 'chat_corpus.txt' if len(sys.argv) < 6  else str(sys.argv[5])
players_name = 'players.csv' if len(sys.argv) < 7  else str(sys.argv[6])
matches_name = 'matches.csv' if len(sys.argv) < 8 else str(sys.argv[7])

# chat_atrs = ['date', 'time', 'sent_to', 'champion_name', 'message', 'association_to_offender', 'name_change'],
# ply_atrs = ['level', 'kills', 'deaths', 'assists', 'gold_earned', 'outcome', 'time_played',
#             'association_to_offender', 'champion_name'],
# match_atrs = ['game_mode', 'game_type', 'premade', 'most_common_report_reason', 'allied_report_count',
#               'enemy_report_count', 'case_total_reports', 'time_played']

chat_atrs = ["association_to_offender", "champion_name", "time", "message"]
player_atrs = ['association_to_offender', 'champion_name', 'kills', 'deaths', 'assists', 'gold_earned', 'outcome']
match_atrs = ['premade', 'most_common_report_reason', 'allied_report_count', 'enemy_report_count', 'case_total_reports',
              'time_played']


def text_consuming(writer, buffer):
	value = buffer.get()
	writer.write(value)
	del value


def csv_consuming(writer, buffer):
	value = buffer.get()
	writer.writerow(value)
	del value[:]


def set_chat_processing(consumers, processors, process_csv=True, process_corpus=True):
	corpus_consumer = None
	chat_consumer = None

	if process_corpus:
		corpus_fl = codecs.open(dest_dir + '/' + chat_corpus_name, 'a', encoding='utf-8')
		corpus_consumer = Consumer(corpus_fl, text_consuming)
		consumers.append(corpus_consumer)

	if process_csv:
		chat_fl = codecs.open(dest_dir + '/' + chat_csv_name, "a", encoding='utf-8')
		chat_wr = csv.writer(chat_fl)
		chat_consumer = Consumer(chat_wr, csv_consuming)
		consumers.append(chat_consumer)

	if process_csv or process_corpus:
		processors.append(ChatProcessor(chat_atrs, chat_consumer, corpus_consumer,
		                                corpus=process_corpus, csv=process_csv,
		                                filters=[lambda e: e['association_to_offender'] == 'offender']))


def set_players_processing(consumers, processors):
	players_fl = codecs.open(dest_dir + '/' + players_name, 'a', encoding='utf-8')
	players_wr = csv.writer(players_fl)
	player_consumer = Consumer(players_wr, csv_consuming)

	consumers.append(player_consumer)
	processors.append(PlayerProcessor(player_atrs, player_consumer, [lambda e: e['association_to_offender'] == 'offender']))


def set_matches_processing(consumers, processors):
	matches_fl = codecs.open(dest_dir + '/' + matches_name, 'a', encoding='utf-8')
	matches_wr = csv.writer(matches_fl)
	match_consumer = Consumer(matches_wr, csv_consuming)

	consumers.append(match_consumer)
	processors.append(MatchProcessor(match_atrs, match_consumer))


# ---------------------Main-----------------

last_thread = None
consumers = []
processors = []
prod_sem = Semaphore(num_producers)

if bool(chat_csv_name) or bool(chat_corpus_name):
	set_chat_processing(consumers, processors, bool(chat_csv_name), bool(chat_corpus_name) )

if bool(players_name):
	set_players_processing(consumers, processors)

if bool(matches_name):
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

print("Esperando pelos consumidores...")
for consumer in consumers:
	consumer.join()

print('Organizando resultados...')
import subprocess

subprocess.call(['bash', 'sort', 'chat.csv', 'chat.csv'])
subprocess.call(['bash', 'sort', 'players.csv', 'players.csv'])
subprocess.call(['bash', 'sort', 'matches.csv', 'matches.csv'])
