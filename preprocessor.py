import string
import re
import unicodedata
from nltk.tokenize import word_tokenize

class Preprocessor(object):

	def __init__(self):
		super().__init__()
		
	def clean(self, sentence):
		self.sentence = sentence
		self.url_remover()
		self.accent_remover()
		self.emoticon_remover()
		self.nonprintable_remover()
		return self.sentence

	def normalize(self,sentence):
		return sentence.lower()

	def tokenize_sentence(self,sentence):
		return word_tokenize(sentence)

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

	def __str__(self):
		return self.sentence

x = Preprocessor()
new_text = x.clean("this Is a :) :D:( O test https://sdfs.sdfsdf.com/sdfsdf/sdfsdf/sd/sdfsdfs?bob=%20tree&jef=man lets see this too https://sdfsdf.fdf.com/sdf/f end")
new_text = x.normalize(new_text)
tokens = x.tokenize_sentence(new_text)

print(new_text)
print(tokens)