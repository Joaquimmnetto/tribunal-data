# encoding=utf8
from multiprocessing import Process
from threading import Thread
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


class ProducersManager(Process):

	def __init__(self, tar_path, processors, prod_semaphore = None):
		Process.__init__(self)
		self.tar_path = tar_path
		self.processors = processors
		self.prod_semaphore = prod_semaphore

	def process_jsons(self,jsons_dir,jsons_name):
		jsonsFile = open(jsons_dir + '/' + jsons_name, 'rt', encoding='utf-8')
		case = []
		case_id = os.path.basename(jsonsFile.name).split('.')[0]
		for match_num, json_str in enumerate(jsonsFile):
			try:
				if json_str.strip().strip('\n').strip('"') == '':
					continue
				match = json.loads(json_str)
				match['case_id'] = case_id
				case.append(match)
			except:
				pass

		return case

	def run(self):
		if self.prod_semaphore is not None:
			self.prod_semaphore.acquire()

		print("Extracting " + str(self.tar_path))
		jsons_dir = TarReader().extract(self.tar_path)

		print("Processing " + str(self.tar_path) + " > " + str(jsons_dir))
		for jsons_name in os.listdir(jsons_dir):
			case = self.process_jsons(jsons_dir, jsons_name)
			for match_num, match in enumerate(case):
				for processor in self.processors:
					try:
						processor.process(match_num, match)
					except:
						print(('Excecao enquanto processando '+str(match['case_id'])+ "-" + str(match_num)))
						traceback.print_exc()

		if self.prod_semaphore is not None:
			self.prod_semaphore.release()
		print((str(jsons_dir) + " closing..."))
		shutil.rmtree(jsons_dir)


