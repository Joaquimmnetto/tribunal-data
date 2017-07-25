# encoding=utf8

from datetime import datetime as dt

from .processor import Processor


class ChatProcessor(Processor):
  def __init__(self, atrs, csv_consumer, corpus_consumer, **kwargs):
    _filters = kwargs['filters'] if 'filters' in kwargs else list()

    Processor.__init__(self, atrs, csv_consumer, _filters)

    self.corpus_consumer = corpus_consumer
    self.csv = kwargs['csv'] if 'csv' in kwargs else True
    self.corpus = kwargs['corpus'] if 'corpus' in kwargs else False

  def create_time_context(self, match, time_window):
    context = list()
    players_buffer = {}
    players_t0 = {}

    for entry in match['chat_log']:
      player = (entry['association_to_offender'], entry['champion_name'])
      timestamp = dt.strptime(entry['time'], "%H:%M:%S")

      if player not in list(players_t0.keys()):
        players_t0[player] = entry

      t0 = dt.strptime(players_t0[player]['time'], "%H:%M:%S")
      if (timestamp - t0).total_seconds() > time_window:
        context_entry = players_t0[player]
        context_entry['message'] = players_buffer[player]
        context.append(context_entry)

        players_buffer[player] = ""
        players_t0[player] = entry

      if player not in list(players_buffer.keys()):
        players_buffer[player] = ""

      players_buffer[player] += entry['message'] + " "

    for player in list(players_buffer.keys()):
      context_entry = players_t0[player]
      context_entry["message"] = players_buffer[player]
      context.append(context_entry)

    context.sort(key=lambda x: x['time'])

    return context

  def process(self, match_num, match):
    csv = self.csv
    corpus = self.corpus

    self.apply_header() if csv else None

    case_id = match['case_id']

    chat = match['chat_log']

    if 'time' in self.atrs and 'message' in self.atrs:
      chat = self.create_time_context(match, 5)

    for entry in chat:
      if not self.apply_filter(entry):
        continue

      if csv:
        csv_array = list()
        csv_array.append(case_id)
        csv_array.append(match_num)
      if corpus:
        corpus_lst = []
      for attr in self.atrs:
        if attr == 'message':
          if not any(entry[attr]):
            csv_array.append("") if csv else None
          else:
            corpus_lst.append(entry[attr]) if corpus else None
            csv_array.append(entry[attr]) if csv else None
        else:
          csv_array.append(entry[attr]) if csv else None

      self.consumer.feed(csv_array) if csv else None

      self.corpus_consumer.feed(' '.join(corpus_lst) + '\n') if corpus else None
