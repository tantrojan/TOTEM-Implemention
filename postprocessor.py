from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
import numpy, math
from collections import Counter

stop_words = stopwords.words('english')
stop_words.extend(['rt'])

class Postprocessor(object):

	threshold = 0.1
	epsilon = 0.1

	def __init__(self):
		super(Postprocessor, self).__init__()
		self.score_centroid = []
		self.score_word_rank = []
		self.score_word_freq = []

	def __call__(self, document):

		sentences_words = []
		bag_of_words = {}
		for sent in document:
			words = []
			for w in word_tokenize(sent):
				if w not in stop_words:
					words.append(w)
					if w not in bag_of_words:
						bag_of_words[w]=1
					else:
						bag_of_words[w]+=1
			sentences_words.append(words)

		bag_of_words = dict(sorted(bag_of_words.items(), key=lambda x: x[1], reverse = True))

		tf_metrics = self._compute_tf(sentences_words)
		idf_metrics = self._compute_idf(sentences_words)

		matrix = self._create_matrix(sentences_words, self.threshold, tf_metrics, idf_metrics)
		

		self.score_centroid = self.power_method(matrix, self.epsilon)
		self.score_word_rank = self.word_rank(bag_of_words,sentences_words)
		self.score_word_freq = self.word_freq(bag_of_words,sentences_words)


	def _compute_tf(self, sentences):
		tf_values = map(Counter, sentences)
		tf_metrics = []
		for sentence in tf_values:
			metrics = {}
			max_tf = self._find_tf_max(sentence)
			for term, tf in sentence.items():
				metrics[term] = tf / max_tf

			tf_metrics.append(metrics)

		# print(tf_metrics)
		return tf_metrics

	@staticmethod
	def _find_tf_max(terms):
		return max(terms.values()) if terms else 1

	@staticmethod
	def _compute_idf(sentences):
	    idf_metrics = {}
	    #total count of sentences - tancount of words in the sentence
	    sentences_count = len(sentences)

	    for sentence in sentences:
	        for term in sentence:
	            if term not in idf_metrics:
	                n_j = sum(1 for s in sentences if term in s)
	                idf_metrics[term] = math.log(sentences_count / (1 + n_j))
	    # print(idf_metrics)
	    return idf_metrics

	def _create_matrix(self, sentences, threshold, tf_metrics, idf_metrics):
	    """
	    Creates matrix of shape |sentences|×|sentences|.
	    """
	    # create matrix |sentences|×|sentences| filled with zeroes
	    sentences_count = len(sentences)
	    matrix = numpy.zeros((sentences_count, sentences_count))
	    degrees = numpy.zeros((sentences_count, ))

	    for row, (sentence1, tf1) in enumerate(zip(sentences, tf_metrics)):
	        for col, (sentence2, tf2) in enumerate(zip(sentences, tf_metrics)):
	            matrix[row, col] = self.cosine_similarity(sentence1, sentence2, tf1, tf2, idf_metrics)

	            if matrix[row, col] > threshold:
	                matrix[row, col] = 1.0
	                degrees[row] += 1
	            else:
	                matrix[row, col] = 0

	    for row in range(sentences_count):
	        for col in range(sentences_count):
	            if degrees[row] == 0:
	                degrees[row] = 1

	            matrix[row][col] = matrix[row][col] / degrees[row]

	    return matrix

	@staticmethod
	def cosine_similarity(sentence1, sentence2, tf1, tf2, idf_metrics):
	    unique_words1 = frozenset(sentence1)
	    unique_words2 = frozenset(sentence2)
	    common_words = unique_words1 & unique_words2

	    numerator = 0.0
	    for term in common_words:
	        numerator += tf1[term]*tf2[term] * idf_metrics[term]**2

	    denominator1 = sum((tf1[t]*idf_metrics[t])**2 for t in unique_words1)
	    denominator2 = sum((tf2[t]*idf_metrics[t])**2 for t in unique_words2)

	    if denominator1 > 0 and denominator2 > 0:
	        return numerator / (math.sqrt(denominator1) * math.sqrt(denominator2))
	    else:
	        return 0.0

	@staticmethod
	def power_method(matrix, epsilon):
	    transposed_matrix = matrix.T
	    sentences_count = len(matrix)
	    p_vector = numpy.array([1.0 / sentences_count] * sentences_count)
	    lambda_val = 1.0

	    while lambda_val > epsilon:
	        next_p = numpy.dot(transposed_matrix, p_vector)
	        lambda_val = numpy.linalg.norm(numpy.subtract(next_p, p_vector))
	        p_vector = next_p

	    return list(p_vector)
		
	@staticmethod
	def word_rank(bag_of_words,sentences_words):

		bag_of_words =list(bag_of_words)
		V = len(bag_of_words)
		score_word_rank = []
		for sent in sentences_words:
			K = len(sentences_words)
			value = 0
			for word in sent:
				value += (V - bag_of_words.index(word) + 1)
			value = value/K
			score_word_rank.append(value)

		# Normalizing (Converting in range 0 and 1)
		max_result = max(score_word_rank)
		score_word_rank = [x/max_result for x in score_word_rank]

		return score_word_rank


	@staticmethod
	def word_freq(bag_of_words,sentences_words):

		Max_word_freq = bag_of_words[list(bag_of_words)[0]]
		score_word_freq = []
		for sent in sentences_words:
			K = len(sentences_words)
			value = 0
			for word in sent:
				value += (Max_word_freq - bag_of_words[word])
			value = value/K
			score_word_freq.append(value)

		# Normalizing (Converting in range 0 and 1)
		max_result = max(score_word_freq)
		score_word_freq = [x/max_result for x in score_word_freq]

		return score_word_freq



		