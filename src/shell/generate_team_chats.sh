grep ',ally,' < ${1} > out/ally_chat.csv
grep ',enemy,' < ${1} > out/enemy_chat.csv
grep ',offender,' < ${1} > out/offender_chat.csv

./csv_text_extractor.sh 6 out/ally_chat.csv > out/ally_corpus.csv
./csv_text_extractor.sh 6 out/enemy_chat.csv > out/enemy_corpus.csv
./csv_text_extractor.sh 6 out/offender_chat.csv > out/offender_corpus.csv




