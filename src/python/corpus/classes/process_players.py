# encoding=utf8
from .processor import Processor


class PlayerProcessor(Processor):

	def __init__(self, atrs, consumer, filters=None):
		Processor.__init__(self, atrs, consumer, filters)

	def process(self, match_num, match):
		self.apply_header()

		case_id = match['case_id']

		for entry in match['players']:
			if not self.apply_filter(entry):
				continue

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
