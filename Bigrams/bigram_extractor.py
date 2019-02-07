file = open('count_2w.txt', 'r')

text = file.read().split('\n')
clean_text = [ x.split('\t')[0] for x in text if not x.startswith('<S>') ]

newfile = open('common_bigrams.txt', 'w')
for i in clean_text:
	newfile.write(i+'\n')