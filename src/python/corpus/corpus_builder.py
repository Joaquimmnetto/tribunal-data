# encoding=utf8

import os
import sys
import csv
# import utils.args_proc as args
import traceback
from multiprocessing import Semaphore

from classes.consumer import Consumer
from classes.matches_producer import ProducersManager
from classes.process_chat import ChatProcessor
from classes.process_players import PlayerProcessor

from classes.process_match import MatchProcessor

print(("Arguments:" + str(sys.argv)))

tars_dir = "../../../dataset/dataset_sample/sample" if len(sys.argv) < 2 else sys.argv[1]
dest_dir = "../../.." if len(sys.argv) < 3 else sys.argv[2]
num_producers = 4 if len(sys.argv) < 4 else int(sys.argv[3])

chat_csv_name = 'chat2.csv' if len(sys.argv) < 5 else str(sys.argv[4])
players_name = 'players2.csv' if len(sys.argv) < 7 else str(sys.argv[6])
chat_corpus_name = 'None' if len(sys.argv) < 6 else str(sys.argv[5])
matches_name = 'matches2.csv' if len(sys.argv) < 8 else str(sys.argv[7])

chat_atrs = ["association_to_offender", "sent_to"]
player_atrs = ['association_to_offender', 'champion_name', 'kills', 'deaths', 'assists', 'gold_earned', 'outcome']
match_atrs = ['game_type', 'most_common_report_reason', 'reports.comments_ally', 'reports.comments_enemy',
              'allied_report_count', 'enemy_report_count', 'time_played']


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
    chat_fl = open(dest_dir + '/' + chat_csv_name, "at", encoding='utf-8', newline="")
    chat_wr = csv.writer(chat_fl)
    chat_consumer = Consumer(chat_wr, csv_consuming)
    consumers.append(chat_consumer)

  if process_csv or process_corpus:
    processors.append(ChatProcessor(chat_atrs, chat_consumer, corpus_consumer,
                                    corpus=process_corpus, csv=process_csv,
                                    filters=[]))


def set_players_processing(consumers, processors):
  players_fl = open(dest_dir + '/' + players_name, 'at', encoding='utf-8', newline="")
  players_wr = csv.writer(players_fl)
  player_consumer = Consumer(players_wr, csv_consuming)

  consumers.append(player_consumer)
  processors.append(PlayerProcessor(player_atrs, player_consumer, filters=[]))


def set_matches_processing(consumers, processors):
  matches_fl = open(dest_dir + '/' + matches_name, 'at', encoding='utf-8', newline="")
  matches_wr = csv.writer(matches_fl)
  match_consumer = Consumer(matches_wr, csv_consuming)

  consumers.append(match_consumer)
  processors.append(MatchProcessor(match_atrs, match_consumer, filters=[]))


# ---------------------Main-----------------
def main():
  consumers = []
  processors = []
  prod_sem = Semaphore(num_producers)

  if chat_csv_name != "None" or chat_corpus_name != "None":
    set_chat_processing(consumers, processors, chat_csv_name != "None", chat_corpus_name != "None")

  if players_name != "None":
    set_players_processing(consumers, processors)

  if matches_name != "None":
    set_matches_processing(consumers, processors)

  print("Iniciando Consumidores, ")
  for consumer in consumers:
    consumer.start()

  producers = []

  for tar_name in os.listdir(tars_dir):
    if not (tar_name.endswith('.tar.gz') and 'jsons' in tar_name):
      continue
    try:
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


import datetime

if __name__ == '__main__':
  before = datetime.datetime.now()
  main()
  print("Time elapsed:", datetime.datetime.now() - before)
