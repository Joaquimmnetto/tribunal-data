# encoding=utf8
from src.python.processor import Processor

class MatchProcessor(Processor):

	def __init__(self, atrs, consumer):
		Processor.__init__(self, atrs, consumer)

	def process(self,match_num, match):
		case_id = match['case_id']
		match_players = []
		csv_array = list()
		csv_array.append(case_id)
		csv_array.append(match_num)
		for atr in self.atrs:
			if atr == 'time_played':
				times = [player['time_played'] for player in match['players']]
				times.sort(reverse=True)
				value = times[0]
			else:
				value = match[atr]
			csv_array.append(value)

		self.consumer.feed(csv_array)

		return match_players
