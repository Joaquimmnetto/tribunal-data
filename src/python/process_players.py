# encoding=utf8
from src.python.processor import Processor


class PlayerProcessor(Processor):

	def __init__(self,atrs, consumer):
		Processor.__init__(self, atrs, consumer)

	def process(self, match_num, match):
		case_id = match['case_id']
		match_players = []

		for entry in match['players']:
			csv_array = list()
			csv_array.append(case_id)
			csv_array.append(match_num)
			for atr in self.atrs:
				value = None
				if atr == 'kills' or atr == 'deaths' or atr == 'assists':
					value = entry['scores'][atr]
				else:
					value = entry[atr]
				csv_array.append(value)

			self.consumer.feed(csv_array)

		return match_players
