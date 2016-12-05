import time
from classes.matches_producer import ProducersManager
from classes.process_telegram_msgs import ProcessTelegramMsg
from classes.consumer import Consumer
import pickle

usr_aliases = {}
chats_usrs = {}
usr_msgs = {}


def consume_msgs(writer,msg):
	usr_id = msg[0]
	chat_id = msg[1]
	usr_alias = msg[2]
	usr_name = msg[3]
	message = msg[4]

	try:
		chats_usrs[chat_id].add(usr_id)
	except:
		chats_usrs[chat_id] = set([usr_id])

	try:
		usr_msgs[usr_id].append(message)
	except:
		usr_msgs[usr_id] = [message]

	usr_aliases[usr_id] = (usr_name,usr_alias)



cons = Consumer(writer=None, consume = consume_msgs)
processor = ProcessTelegramMsg(consumer = cons)
prod = ProducersManager(tar_path = 'telegram_corpus.tar.gz',processors=[processor])

cons.start()
prod.start()
prod.join()
print("Producer finished.")
cons.stop()
cons.join()


#time.sleep(20)
print("Writing dictionaries...")
for usr_id in usr_msgs.keys():
	with open('usr_corpora/'+str(usr_id)+".crp",'w',encoding='utf-8') as fl:
		msgs = '\n'.join(usr_msgs[usr_id])
		fl.write(msgs)


with open("users.pkl",'wb') as fl:
	pickle.dump(usr_aliases, fl, pickle.HIGHEST_PROTOCOL)

with open("chat_users.pkl", 'wb') as fl:
	pickle.dump(chats_usrs, fl, pickle.HIGHEST_PROTOCOL)







