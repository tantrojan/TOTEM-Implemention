import string
import re
import unicodedata
from nltk.tokenize import word_tokenize
from string import punctuation
import csv

class Preprocessor(object):

	def __init__(self):
		super().__init__()
		self.slang_dictionary = {}

		# Creating Slang Dictionary
		csvfile = open('./Slang Words/noslang.csv','r')
		reader = csv.reader(csvfile)
		for row in reader:
			self.slang_dictionary[str(row[0])] = str(row[1])
	
	# URLs are removed, Removing special characters which has different accent and emoticons, non-printable ASCII characters are removed. The cleaned text is tokenized.
	def clean(self, sentence):
		self.sentence = sentence

		# Removers
		self.url_remover()
		self.accent_remover()
		self.emoticon_remover()
		self.nonprintable_remover()

		# Convert lowercase
		self.sentence = self.sentence.lower()

		# Remove punctuations
		exclude = set(string.punctuation)
		self.sentence = ''.join(ch for ch in self.sentence if ch not in exclude)

		self.replace_slangs()

		# Tokenize
		tokens = word_tokenize(self.sentence)
		del self.sentence
		return tokens

	def url_remover(self):
		self.sentence = re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', '', self.sentence)
	
	def accent_remover(self):

		text = self.sentence

		try:
			text = unicode(text, 'utf-8')
		except (TypeError, NameError):
			pass
		text = unicodedata.normalize('NFD', text)
		text = text.encode('ascii', 'ignore')
		text = text.decode("utf-8")
		
		self.sentence = text
		del text

	def emoticon_remover(self):
		self.sentence = re.sub(r'''(?:X|:|;|=)(?:-)?(?:\)|\(|O|D|P|S){1,}''', '', self.sentence)

		try:
			self.sentence = re.sub(r'''([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])''', '', self.sentence)
		except re.error:
			self.sentence = re.sub(r'''([\u2600-\u27BF])|([\uD83C][\uDF00-\uDFFF])|([\uD83D][\uDC00-\uDE4F])|([\uD83D][\uDE80-\uDEFF])''', '', self.sentence)

	def nonprintable_remover(self):
		self.sentence = ''.join([x if x in string.printable else '' for x in self.sentence])

	def replace_slangs(self):

		for word in word_tokenize(self.sentence):
			# print(word)
			if word in self.slang_dictionary:
				print(self.slang_dictionary[word])
				self.sentence = re.sub(r'\b'+word+r'\b', self.slang_dictionary[word],self.sentence)
		


