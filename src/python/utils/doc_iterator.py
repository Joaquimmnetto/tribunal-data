import csv

class DocIterator(object):

	def __init__(self, chat_fn, corpus_fn):
		self.chat_fn = chat_fn
		self.corpus_fn = corpus_fn

	def next_doc(self):
		i = 0
		with open(self.chat_fn) as cht, open(self.corpus_fn) as crp:
			csv_rd = csv.reader(cht)
			case = 0
			match = 0
			chats = {'ally': list(), 'enemy': list(), 'offender': list()}

			for row, crp_line in zip(csv_rd, crp):
				i+=1
				next_case = int(row[0])
				next_match = int(row[1])
				team = row[2]
				if team.strip() == '':
					continue

				if next_case != case or next_match != match:
					if case != 0:
						ally_doc = ' '.join(chats['ally'])
						enemy_doc = ' '.join(chats['enemy'])
						offender_doc = ' '.join(chats['offender'])

						yield case, match, 'ally', ally_doc
						yield case, match, 'enemy', enemy_doc
						yield case, match, 'offender', offender_doc

					del chats
					chats = {'ally': list(), 'enemy': list(), 'offender': list()}
					match = next_match
					case = next_case

				chats[team].append(crp_line.strip('\n'))
