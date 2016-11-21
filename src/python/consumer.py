# encoding=utf8
from queue import Queue
from threading import Thread


class Consumer(Thread):

	def __init__(self,writer,consume):
		Thread.__init__(self)

		self.writer = writer
		self.consume = consume

		self.buffer = Queue()
		self.stop = False

	def feed(self,value):
		self.buffer.put(value)

	def stop(self):
		self.stop = True

	def run(self):
		while not (self.stop and self.buffer.empty()):
			self.consume(self.writer, self.buffer)

		print('consumer stopped')
		self.writer.close()




