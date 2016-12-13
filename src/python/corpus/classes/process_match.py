# encoding=utf8
from .processor import Processor

class MatchProcessor(Processor):



	def __init__(self, atrs, consumer, filters=None):
		Processor.__init__(self, atrs, consumer, filters)

	def process(self,match_num, match):
		self.apply_header()

		if not self.apply_filter(match):
			return False

		case_id = match['case_id']
		csv_array = list()
		csv_array.append(case_id)
		csv_array.append(match_num)
		reports = {'ally':'','enemy':''}

		if ('reports.comments_ally' in self.atrs) or ('reports.comments_enemy' in self.atrs):
			for report in match['reports']:
				if report['association_to_offender'] == 'ally':
					reports['ally']+= report['comment']
				elif report['association_to_offender'] == 'enemy':
					reports['enemy'] += report['comment']
			pass

		for atr in self.atrs:
			if atr == 'time_played':
				times = [player['time_played'] for player in match['players']]
				times.sort(reverse=True)
				value = times[0]
			elif atr == 'reports.comments_ally':
				value = reports['ally'].replace('\n',' ')
			elif atr == 'reports.comments_enemy':
				value = reports['enemy'].replace('\n',' ')
			else:
				value = match[atr]
			csv_array.append(value)

		self.consumer.feed(csv_array)
