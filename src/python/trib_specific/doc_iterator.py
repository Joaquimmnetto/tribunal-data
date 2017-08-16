import csv


class DocIterator(object):
  def __init__(self, chat_fn, corpus_fn, timeslice_size=-1):
    self.chat_fn = chat_fn
    self.corpus_fn = corpus_fn
    self.timeslice_size = timeslice_size

  def next_doc(self):
    i = 0
    with open(self.chat_fn) as cht, open(self.corpus_fn) as crp:
      csv_rd = csv.reader(cht)
      case = 0
      match = 0
      chats = {'ally': list(), 'enemy': list(), 'offender': list()}
      for row, crp_line in zip(csv_rd, crp):
        i += 1
        if len(row) == 0:
          print(i)
          continue

        try:
          next_case = int(row[0])
          next_match = int(row[1])
        except ValueError:
          continue

        team = row[2]
        if team.strip() == '':
          continue

        timestamp = row[4]
        if not timestamp.isdigit():
          continue

        timeslice = int(int(timestamp) / self.timeslice_size)

        if next_case != case or next_match != match:
          if case != 0:
            if self.timeslice_size < 0:
              ally_doc = [' '.join(chats['ally'])]
              enemy_doc = [' '.join(chats['enemy'])]
              offender_doc = [' '.join(chats['offender'])]
            else:
              ally_doc = [' '.join(slice) for slice in chats['ally']]
              enemy_doc = [' '.join(slice) for slice in chats['enemy']]
              offender_doc = [' '.join(slice) for slice in chats['offender']]

            yield case, match, 'ally', ally_doc
            yield case, match, 'enemy', enemy_doc
            yield case, match, 'offender', offender_doc

          del chats
          chats = {'ally': list(), 'enemy': list(), 'offender': list()}
          match = next_match
          case = next_case

        line = crp_line.strip('\n')

        if self.timeslice_size < 0:
          chats[team].append(line)
        else:
          if len(chats[team]) - 1 < timeslice:
            for _ in range(len(chats[team]), timeslice + 1):
              chats[team].append(list())

          chats[team][timeslice].append(line)
