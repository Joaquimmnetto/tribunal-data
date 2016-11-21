# encoding=utf8
from threading import Thread
from threading import Semaphore
import codecs
import random
import string
import os
import tarfile
import json
import traceback
import shutil
import time



class TarReader():

	def __init__(self):
		self.tmp_dir = "tmp/" + ''.join(random.choice(string.ascii_lowercase) for i in range(5))

	def extract(self,tar_path):
		os.mkdir(self.tmp_dir)

		game_tar = tarfile.open(tar_path, 'r:gz')
		game_tar.extractall(self.tmp_dir)

		game_tar.close()

		return self.tmp_dir


class ProducersManager(Thread):

	def __init__(self, jsons_dir, processors, prod_semaphore):
		Thread.__init__(self)
		self.jsons_dir = jsons_dir
		self.processors = processors
		self.prod_semaphore = prod_semaphore

	def process_jsons(self,jsons_name):
		jsonsFile = codecs.open(self.jsons_dir + '/' + jsons_name, 'rb')
		case = []
		case_id = os.path.basename(jsonsFile.name).split('.')[0]
		for match_num, json_str in enumerate(jsonsFile):
			try:
				json_str = json_str.decode('utf-8')
				if json_str.strip().strip('\n').strip('"') == '':
					continue
				match = json.loads(json_str)

				match['case_id'] = case_id
				case.append(match)

			except:
				print(('Erro na formatacao do arquivo '+jsons_name))
				return []

		return case

	def run(self):
		num_permits = 4
		processor_sem = Semaphore(num_permits)

		for jsons_name in os.listdir(self.jsons_dir):
			case = self.process_jsons(jsons_name)
			for match_num, match in enumerate(case):
				for processor in self.processors:
					try:
						processor.set_params(match_num,match,processor_sem)
						processor_sem.acquire()
						processor.start()
					except:
						print(('Excecao enquanto processando '+str(match['case_id'])+ "-" + str(match_num)))
						traceback.print_exc()

		for processor in self.processors:
			processor.join()

		self.prod_semaphore.release()
		print((str(self.jsons_dir) + " closing..."))
		shutil.rmtree(self.jsons_dir)


