'''
Performs various basic word analysis on an input of a list of words.

Available Keyword Arguments:
- reverse=True

Current Functionality:
- Alphabetize: returns an alphabetically sorted list
- Word Count:  returns a dictionary containing the frequency of words


'''
class WordAnalyzer:
	def __init__(self, words, *args, **kwargs):
		self.words = words
		word = self.alphabetize()
		print(word)

	def alphabetize(self):
		return sorted(self.words)

	def word_count(self):
		word_freq = {}

		for word in self.words:
			if word in word_freq.keys():
				word_freq[word] += 1
			else:
				word_freq[word] = 1

		return word_freq


