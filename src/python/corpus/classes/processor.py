# encoding=utf8

from threading import Thread
import traceback


class Processor:
  def __init__(self, atrs, consumer, filters=None):
    self.atrs = atrs
    self.consumer = consumer
    self.filters = filters if filters is not None else []
    self.header = True
    self.threads = []

  def add_filter(self, cmp_lmb):
    self.filters.append(cmp_lmb)

  def apply_filter(self, entry):
    valid = True

    for fltr in self.filters:
      if not fltr(entry):
        valid = False
        break

    return valid

  def process(self, match_num, match):
    pass

  def apply_header(self):
    pass
    if not self.header:
      headers = ['case', 'match'] + self.atrs
      self.consumer.feed(headers)
      self.header = True


      # def set_params(self,match_num,match,semaphore):
      # 	self.match_num = match_num
      # 	self.match = match
      # 	self.semaphore = semaphore
      #
      # def run(self,match_num,match,thread):
      # 	try:
      # 		self.process(match_num,match)
      # 	except:
      # 		traceback.print_exc()
      # 	finally:
      # 		self.semaphore.release()
      #
      # def start(self):
      # 	current_thread = Thread(target=self.run,args=(self.match_num,self.match))
      # 	self.threads.append(current_thread)
      # 	current_thread.start()
      #
      # def join(self):
      # 	for t in self.threads:
      # 		if t.is_alive():
      # 			t.join()
