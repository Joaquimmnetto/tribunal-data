import datetime
import args_proc as args


def bigramize(corpus, out):
  for line in corpus:
    words = line.split()

    next_words = words[1:len(words)]
    words = words[0:len(words) - 1]

    bigrams = [w + "_" + next_words[i] for i, w in enumerate(words)]

    out.write(' '.join(bigrams) + "\n")


# O que fazer com as expressões de uma única linha?
# manter?descartar?
before = datetime.datetime.now()
bigramize(open(args.corpus), open(args.bigrams(args.corpus), 'w'))
print("Time elapsed:", datetime.datetime.now() - before)
