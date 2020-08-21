'''
Performs various basic word analysis on an input of a list of words.

Available Keyword Arguments:
- reverse=True

Current Command Functionality:
- alphabetize: returns an alphabetically sorted list
- word-count:  returns a dictionary containing the frequency of words


'''
class WordAnalyzer:
	def __init__(self, words, movie_name, *args, **kwargs):
		self.words = words
		self.movie_name = movie_name
		self.save = False

		# Most keywords default to false.  Command defaults to alphabetize
		self.reverse = kwargs.get('reverse', False)

	def alphabetize(self):
		return sorted(self.words) if self.reverse == False else sorted(self.words, reverse=True)

	def word_count(self):
		''' 
		Note that reverse doesn't matter. It is up to the user to do what they
		want since this is a count.
		'''
		word_freq = {}

		for word in self.words:
			if word in word_freq.keys():
				word_freq[word] += 1
			else:
				word_freq[word] = 1

		return word_freq


