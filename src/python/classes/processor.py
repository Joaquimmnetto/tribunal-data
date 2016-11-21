# encoding=utf8

from threading import Thread


class Processor:

	def __init__(self, atrs, consumer, filters=None):
		self.atrs = atrs
		self.consumer = consumer
		self.filters = filters if filters is not None else []

	def add_filter(self,cmp_lmb):
		self.filters.append(cmp_lmb)

	def apply_filter(self,entry):
		invalid = False

		for fltr in self.filters:
			if not fltr(entry):
				invalid = True
				break

		return invalid

	def process(self,match_num,match):
		pass

	def set_params(self,match_num,match,semaphore):
		self.match_num = match_num
		self.match = match
		self.semaphore = semaphore

	def run(self,match_num,match):
		self.process(match_num,match)
		self.semaphore.release()

	def start(self):
		self.current_thread = Thread(target=self.run,args=(self.match_num,self.match))
		self.current_thread.start()

	def join(self):
		if self.current_thread.is_alive():
			self.current_thread.join()