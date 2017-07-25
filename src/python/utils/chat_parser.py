import args_proc as args
import pandas

def parse_time(timestamp):
  if type(timestamp) is str:
    ts = timestamp.split(':')
    h, m, s = [int(i) for i in ts]
    seconds = h * 3600 + m * 60 + s
    return seconds
  return 0


def main():
  chat_file = open(args.chat, 'r')
  outp_file = open(args.chat_parsed, 'w')
  # chat_df = pandas.read_csv(args.chat, usecols=range(5),
  #                           names=['case', 'match', 'relation.offender', 'champion', 'timestamp'],
  #                           header=None, error_bad_lines=False, warn_bad_lines=True, skip_blank_lines=True)

  chat_chunks = pandas.read_table(chat_file, chunksize=10000000, lineterminator='\n', quotechar='\"', sep=',',
                                  usecols=range(5),
                                  names=['case', 'match', 'relation.offender', 'champion', 'timestamp'],
                                  header=None, error_bad_lines=False, warn_bad_lines=True, skip_blank_lines=True)

  for i, chunk in enumerate(chat_chunks):
    print("processing chunk ", i)
    chat_df = pandas.DataFrame(chunk)
    print('Convertendo timestamps')
    chat_df['timestamp'] = chat_df['timestamp'].apply(parse_time)
    chat_df.to_csv(outp_file, index=False, header=False)


if __name__ == '__main__':
  args.measure_time(main)
