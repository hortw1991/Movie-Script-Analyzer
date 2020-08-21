'''
Performs various basic word analysis on an input of a list of words.

Current Functionality:
- Alphabetize: returns an alphabetically sorted list
- Word Count:  returns a dictionary containing the frequency of words


'''
class WordAnalyzer:
	def __init__(self, words, flag='alphabetize', save=False, save_location=None):
		self.words = words
		self.flag = flag
		self.save = save
		self.save_location = save_location


		
