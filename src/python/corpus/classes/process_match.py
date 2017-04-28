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
		reports = {'ally':[], 'enemy':[]}

		if ('reports.comments_ally' in self.atrs) or ('reports.comments_enemy' in self.atrs):
			for report in match['reports']:
				if report['association_to_offender'] == 'ally':
					reports['ally'].append(report['comment']) if len(report['comment'].strip()) > 0 else None
				elif report['association_to_offender'] == 'enemy':
					reports['enemy'].append(report['comment']) if len(report['comment'].strip()) > 0 else None
			pass

		for atr in self.atrs:
			if atr == 'time_played':
				times = [player['time_played'] for player in match['players']]
				times.sort(reverse=True)
				value = times[0]
			elif atr == 'reports.comments_ally':
				value = '.'.join(reports['ally']).replace('\n','').replace('\r','') if len(reports['ally']) > 0 else ""
			elif atr == 'reports.comments_enemy':
				value = '.'.join(reports['enemy']) if len(reports['enemy']) > 0 else ""
			else:
				value = match[atr]

			csv_array.append(value)

		self.consumer.feed(csv_array)
