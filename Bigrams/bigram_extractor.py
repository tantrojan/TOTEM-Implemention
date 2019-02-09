from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

print(stop_words)

file = open('count_2w.txt', 'r')

text = file.read().split('\n')
clean_bigrams = [ x.split('\t')[0].lower() for x in text if not x.startswith('<S>') ]

# print(clean_bigrams[0].split(' ')[0] not in stop_words)
filtered_bigrams = []
for bigram in clean_bigrams:
	words = bigram.split(' ')
	# print(words[0])
	# print(words[1])
	if words[0] not in stop_words and words[1] not in stop_words:
		filtered_bigrams.append(bigram)

newfile = open('common_bigrams.txt', 'w')
for i in filtered_bigrams:
	newfile.write(i+'\n')