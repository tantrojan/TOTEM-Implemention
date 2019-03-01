import sys
from preprocessor import Preprocessor
from postprocessor import Postprocessor
from nltk.tokenize import sent_tokenize


class Totem(object):
	"""docstring for Totem"""
	def __init__(self, document):
		super(Totem, self).__init__()
		self.filename = document
		self.sentences = []
		self.preprocessed_sentences = []
		self.bag_of_words = []
		self.hash_counts = []
		self.score_centroid = []
		self.score_word_rank = []
		self.score_word_freq = []
		self.total_score = []

	def __call__(self):
		self.preprocess_doc()
		self.postprocess_doc()
		self.scoring()

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
			self.bag_of_words.append(preprocessor.tokens)
			self.hash_counts.append(preprocessor.hash_count)

		# Normalizing (Converting in range 0 and 1)
		max_result = max(self.hash_counts)
		self.hash_counts = [x/max_result for x in self.hash_counts]


	def postprocess_doc(self):

		postprocessor = Postprocessor()
		postprocessor(self.sentences)
		self.score_centroid = postprocessor.score_centroid 
		self.score_word_rank = postprocessor.score_word_rank
		self.score_word_freq = postprocessor.score_word_freq

	def scoring(self):

		for i in range(len(self.score_word_rank)):
			self.total_score.append(self.score_centroid[i] + self.score_word_rank[i] + self.score_word_freq[i] + self.hash_counts[i])

		ranking = sorted(list(zip(self.sentences,self.total_score)), key = lambda x : x[1], reverse = True)

		for i in ranking:
			print(i)
		


def main():
	program_name = sys.argv[0]
	arguments = sys.argv[1:]
	
	if len(arguments) != 1:
		print("Invalid number of arguments. Exiting.")
		sys.exit()

	document = arguments[0]
	summarizer = Totem(document)
	summarizer()
	




if __name__ == "__main__":
	main()