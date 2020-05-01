import sys
from preprocessor import Preprocessor
from topic_modeler import Topic_modeler
from postprocessor import Postprocessor
from nltk.tokenize import sent_tokenize
import time

class Totem(object):
	"""docstring for Totem"""
	def __init__(self, document, output_file, topics):
		super(Totem, self).__init__()
		self.filename = document
		self.sentences = []
		self.output_file = output_file
		self.topics = topics


		# Preprocessed Document
		self.preprocessed_sentences = []
		self.list_of_tokens = []

		# Topicwise divided Document
		self.document_topicwise = {}

		# Scoring Parameters
		self.hash_counts = []
		self.score_centroid = []
		self.score_word_rank = []
		self.score_word_freq = []
		self.ranking = []

	def __call__(self):

		# Preprocessing the complete Document
		self.preprocess_doc()

		# Topic Modelling
		topic_modeler = Topic_modeler()
		self.document_topicwise = topic_modeler(self.preprocessed_sentences, self.list_of_tokens, self.topics)

		# print(self.document_topicwise)

		# Postprocessing and Scoring for each topic separately
		for i in self.document_topicwise:
			self.postprocess_doc(self.document_topicwise[i])
			self.scoring(self.document_topicwise[i])
			self.generate_summary(i+1)

	def preprocess_doc(self):

		with open(self.filename, 'r') as file:
			data=file.read()

		self.sentences = data.split('\n')
		self.sentences = [x for x in self.sentences if len(x)>15]
		# print(self.sentences)

		preprocessor = Preprocessor()
		for i,sent in enumerate(self.sentences):
			preprocessor(sent)
			self.preprocessed_sentences.append(preprocessor.sentence)
			self.list_of_tokens.append(preprocessor.tokens)
			self.hash_counts.append(preprocessor.hash_count)

		# Normalizing (Converting in range 0 and 1)
		max_result = max(self.hash_counts)
		if max_result == 0:
			max_result=1
		self.hash_counts = [x/max_result for x in self.hash_counts]


	def postprocess_doc(self, topic_document):

		postprocessor = Postprocessor()
		postprocessor(topic_document)
		self.score_centroid = postprocessor.score_centroid
		self.score_word_rank = postprocessor.score_word_rank
		self.score_word_freq = postprocessor.score_word_freq

	def scoring(self, topic_document):

		total_score = []

		for i in range(len(self.score_word_rank)):
			total_score.append(self.score_centroid[i] + self.score_word_rank[i] + self.score_word_freq[i] + self.hash_counts[i])

		self.ranking = sorted(list(zip(topic_document, total_score)), key = lambda x : x[1], reverse = True)

	def generate_summary(self,count):
		file = open(self.output_file,'a')
		file.write('Top sentences from Topic {}:\n'.format(count))
		for i in range(4):
			file.write(self.ranking[i][0] + '\n')

		file.close()




def main():
	print('Start')
	start_time = time.time()
	program_name = sys.argv[0]
	arguments = sys.argv[1:]

	if len(arguments) < 2:
		print("Invalid number of arguments. Exiting.")
		sys.exit()

	document = arguments[0]
	output_file = arguments[1]
	topics = arguments[2]
	# print(output_file)

	summarizer = Totem(document, output_file, topics)
	summarizer()

	elapsed_time = time.time() - start_time
	print('End')
	print('Time Elapsed : {}'.format(elapsed_time))




if __name__ == "__main__":
	main()
