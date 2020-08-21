"""
This program takes the URL of a movie script from IMSDb, and then it repeats
it to you, but in alphabetical order (preserving case) or whatever other
option you want.

This main function will retrieve a movie script but does not perform any
analysis itself.  I kept the word analysis class separate for reuse.

Why?  Man should not ask why, but why not.  But really I just needed to get the
brain juices flowing before classes started, and IMSDb does not have an API,
and it's search results do not change the URL, meaning you can't just feed
it query parameters.

Usage:  python [optional flags] -m movie/url

	--search  Optional flag that indicates you want to search and the program 
			  will return the top movie hit.  Results not guaranteed.

	--intact  Optional flag that will actually just retrieve a script for you
			  without performing any input.  This will print the script as
			  written by the writer and render and further commands irrelevant
			  as they rely on eliminating whitespace.  This can be used with 
			  the --save flag to produce {movie}_intact_script.txt

	--save    Optional flag that will save the output to directory with a file
	 		  name {movie}_{command}.txt
	
	--reverse Optional flag that will reverse the command output.

	--command Optional but reccomended command to peform.  See the WordAnalyzer 
	          class for a list of options.  Default is to return an alphabetized 
			  list.  This command supports multiple sequential arguments.

	--movie   [REQUIRED] The movie to return.  
"""

from word_analyzer import WordAnalyzer

from bs4 import BeautifulSoup
from googlesearch import search
import requests
import argparse
import sys
import os

def main(args):
	base_url = r'https://www.imsdb.com/'

	# Retrieve the URL
	if args.search:
		url = search_movie(base_url, args.movie)
	else:
		url = args.movie
	
	r = requests.get(url)
	if r.status_code != 200:
		print("Error!  Bad response")
		sys.exit(0)

	script_text = parse_html(r.text, args.intact)
	
	# Print and quit if they just want raw output.  We will destroy the
	# formatting if we perform any text manipulation.
	if args.intact:
		print_result(script_text)
		if args.save:
			save_intact_result(script_text, args.movie, args.save)
	else:
		# Check for the type of command - default is to print it in alphabetical
		script_words = get_words(script_text)
		analyzer = WordAnalyzer(script_words, args.movie, save=args.save, reverse=args.reverse)

		# List of available commands that will call the function if exists in
		# the WordAnalyzer class.
		commands = {
			'alphabetize': analyzer.alphabetize,
			'word-count': analyzer.word_count
		}

		if not args.command:
			print_result(analyzer.alphabetize())
		else:
			for command in args.command:
				if command not in commands.keys():
					print("Error executing command.  Make sure it exists!")
					continue
				# Get result and save if requested
				output = commands[command]()

				print_result(output)

				if args.save:
					save_command_result(output, command, args.movie, args.save)
		

def search_movie(base_url, movie):
	'''
	Retrieves the URL of the top search term.  This is just a cursory Google
	search grabbing the top link.
	'''
	# We only want results from our base ULR
	query = f'site:{base_url} {movie}'
	res = search(query, tld='com', lang='eng', num=1, start=0, stop=1, pause=2.0)
	if not res:
		print("No results found.  Try a new search.")
		sys.exit(0)
	
	# Slight accuracy check
	url = next(res)
	if 'scripts' not in url:
		print("No IMSDb results found.  Try a new search.")
		sys.exit(0)

	return url


def parse_html(text, intact=False):
	''' 
	Retrieves all <pre> tags into a string and returns a list.  Text is contained
	in both <b> tags and raw HTML between <b> tags.
	This will strip all whitespace if intact is not requested so we can do
	funky things to it.
	'''
	soup = BeautifulSoup(text, 'xml')
	if intact:
		script_text = [item.text for item in soup.find_all('pre')]
	else:
		script_text = [item.text.strip() for item in soup.find_all('pre')]
	
	return script_text
		

def get_words(script_text):
	'''
	Returns a list of words in the script.
	'''

	# Make sure we strip it, intact doesn't matter at this point
	lines = [word.strip() for word in script_text]
	words_list = []
	words = []

	# This list is 3 deep since BS4 retrieved the <pre> tag.  This was necessary
	# because IMSDb does not put most text in <p> and leaves it as raw HTML
	# between <b> tags.
	for l in lines:
		words_list.append(l.split(' '))
	
	# Now grab the actual words and strip out any whitespace
	for word in words_list:
		for w in word:
			if w.isalnum():
				words.append(w)
	
	return words


def save_intact_result(text, movie_name, save_location):
	""" Saves the output to a file line by line. """
	if not os.path.isdir(save_location):
		print("Please enter a directory!")
		sys.exit(0)
	
	file_name = f'{movie_name}_intact_script.txt'
	save_path = os.path.join(save_location, file_name)

	with open(save_path, 'w+') as f:
		for line in text:
			f.write(line)


def save_command_result(text, command, movie_name, save_location):
	""" Saves the output to a file line by line. """
	if not os.path.isdir(save_location):
		print("Please enter a directory!")
		sys.exit(0)
	
	file_name = f'{movie_name}_{command}_script.txt'
	save_path = os.path.join(save_location, file_name)

	with open(save_path, 'w+') as f:
		# Check if it is a dictionary
		if isinstance(text, dict):
			for k, v in text.items():
				f.write(f'{k}: {v}')
		else:
			for line in text:
				print(line)
				f.write(line)


def print_result(text):
		if isinstance(text, dict):
			for k, v in text.items():
				print(f'{k}: {v}')
		else:
			for line in text:
				print(line)


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--search', action='store_true',
						help='An optional flag that retrieves the top search result.')

	parser.add_argument('--intact', action='store_true',
						help='An optional flag that will not analyze the result and\
							  will leave the script intact with whitespace.')

	parser.add_argument('--reverse', action='store_true',
						help='An optional flag that reverses the output order.')

	parser.add_argument('--save', action='store', type=str,
	                    help='An optional flag indicating directory to save the output to.')

	parser.add_argument('--command', action='store', type=str, nargs='*',
						help='An optional but recommended argument that defaults\
							  to return an alphabetized list of words in the script.  \
							  See the WordAnalyzer class for commands.')

	parser.add_argument('--movie', action='store', type=str, required=True,
						help='The URL to the movie script, or the desired search term\
							  if the --s flag is set.')

	args = parser.parse_args()
	main(args)	




