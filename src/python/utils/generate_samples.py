import csv
import datetime
import threading
from multiprocessing import Queue
import args_proc as args
import traceback

smpl_dir = args.model_dir+"/samples"

matches_smpl_fn = smpl_dir+"/matches.csv"
players_smpl_fn = smpl_dir+"/players.csv"
chat_smpl_fn = smpl_dir+"/chat.csv"


class NextMatchWr(threading.Thread):
	def __init__(self,csv_rd,csv_wr):
		threading.Thread.__init__(self)
		self.i = 0
		self.matches = Queue()
		self.mstop = False
		self.csv_rd = csv_rd
		self.csv_wr = csv_wr
		self.daemon = True

	def run(self):
		while not (self.mstop and self.matches.empty()):
			try:
				if self.mstop:
					item = self.matches.get_nowait()
				else:
					item = self.matches.get()

				print(self.matches.qsize())
				self.write_next_match(self.csv_rd,self.csv_wr,item[0],item[1])
			except:
				traceback.print_exc()

		print('consumer stopped',self.matches.qsize())

	def add_next_match(self,case,match):
		self.matches.put(tuple([case,match]))

	def write_next_match(self, csv_rd, csv_wr, mcase, mmatch):
		res = []
		row = []
		try:
			while True:
				row = next(csv_rd)
				case = int(row[0])
				match = int(row[1])
				if (case,match) == (mcase,mmatch) or (case==mcase and match > mmatch) or (case > mcase):
					break

			#00:14:12
			while True:
				case = int(row[0])
				match = int(row[1])
				if (case,match) == (mcase,mmatch):
					res.append(row)
				else:
					break
				row = next(csv_rd)

			csv_wr.writerows(res)

		except StopIteration:
			print(mcase,mmatch)
		except:
			traceback.print_exc()

players = csv.reader(open(args.players))
chat = csv.reader(open(args.chat))
players_smpl = csv.writer(open(players_smpl_fn, 'w'))
chat_smpl = csv.writer(open(chat_smpl_fn, 'w'))

players_cons = NextMatchWr(players,players_smpl)
chat_cons = NextMatchWr(chat,chat_smpl)


def create_samples(matches_smpl_fn):
	with open(matches_smpl_fn) as inp:
		matches = csv.reader(inp)
		for row in matches:
			case = int(row[0])
			match = int(row[1])
			players_cons.add_next_match(case,match)
			chat_cons.add_next_match(case,match)


def main():

	before = datetime.datetime.now()
	print("This program requires that the inputs be sorted by case and match")
	print("Starting consumers thread...")
	players_cons.start()
	chat_cons.start()
	print("Starting the sample creation...")
	create_samples(matches_smpl_fn)
	print("Subtotal time elapsed:", datetime.datetime.now() - before)

	print("Waiting for consumers to finish...")
	players_cons.mstop = True
	chat_cons.mstop = True

	players_cons.join()
	chat_cons.join()
	print("Total time elapsed:", datetime.datetime.now() - before)


if __name__ == '__main__':
	main()