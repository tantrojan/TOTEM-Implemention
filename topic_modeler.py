from gensim import corpora, models

class Topic_modeler(object):
	"""docstring for Topic_modeler"""
	def __init__(self):
		super(Topic_modeler, self).__init__()

	def __call__(self, document, document_token):

		dictionary = corpora.Dictionary(document_token)
		# print(dictionary.token2id)
		dictionary.filter_extremes(no_below=15, no_above=0.5, keep_n=100000)

		corpus = [dictionary.doc2bow(text) for text in document_token]
		# print(corpus)
		ldamodel = models.ldamodel.LdaModel(corpus, num_topics=3, id2word = dictionary, passes=20)
		# print(ldamodel.print_topics(num_topics=3, num_words=3))

		tfidf = models.TfidfModel(corpus)
		corpus_tfidf = tfidf[corpus]

		# lda_model = models.LdaMulticore(bow_corpus, num_topics=10, id2word=dictionary, passes=2, workers=2)

		topic_sentences = {0:[],1:[],2:[]}

		for iterator,i in enumerate(ldamodel[corpus]):
			index = (sorted(i, key=lambda x : x[1], reverse = True)[0][0])
			sentence = document[iterator]
			topic_sentences[index].append(sentence)

		return topic_sentences