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
		self.bag_of_words = []

	def __call__(self):
		self.preprocess_doc()
		self.postprocess_doc()

	def preprocess_doc(self):

		with open(self.filename, 'r') as file:
			data=file.read()

		self.sentences = data.split('\n')
		self.sentences = [x for x in self.sentences if len(x)>15]
		# print(self.sentences)

		preprocessor = Preprocessor()
		for i,sent in enumerate(self.sentences):
			preprocessor(sent)
			self.sentences[i]=preprocessor.sentence;
			self.bag_of_words.append(preprocessor.tokens)

	def postprocess_doc(self):
		postprocessor = Postprocessor()
		postprocessor(self.sentences)



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