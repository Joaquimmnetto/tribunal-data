import traceback
from .processor import Processor


class ProcessTelegramMsg(Processor):
  def __init__(self, atrs=[], consumer=None, filters=None):
    Processor.__init__(self, atrs, consumer, filters)
    pass

  def process(self, match_num, match):
    if not self.apply_filter(match):
      return False

    if match['service'] or match['event'] != 'message' or 'text' not in match.keys():
      return False

    try:
      usr_id = match['from']['peer_id']
      chat_id = match['to']['peer_id']
      usr_alias = match['from']['username'] if 'username' in match['from'].keys() else ''
      usr_name = match['from']['print_name']
      message = match['text'].replace('\n', ' ')
      self.consumer.feed([usr_id, chat_id, usr_alias, usr_name, message])
    except:
      traceback.print_exc()
      return False
