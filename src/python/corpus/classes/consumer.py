# encoding=utf8
from multiprocessing import Queue
from threading import Thread
import traceback


class Consumer(Thread):

	def __init__(self,writer,consume):
		Thread.__init__(self)

		self.writer = writer
		self.consume = consume
		self.daemon = True
		self.buffer = Queue()
		self.mstop = False

	def feed(self,value):
		self.buffer.put(value)

	def stop(self):
		self.mstop = True

	def run(self):
		while not (self.mstop and self.buffer.empty()):
			try:
				if self.mstop:
					item = self.buffer.get_nowait()
				else:
					item = self.buffer.get()

				self.consume(self.writer, item)
			except:
				traceback.print_exc()

		print('consumer stopped',self.buffer.qsize())
		#self.writer.close()




