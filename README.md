# Movie-Script-Analyzer

## What?

This script retrieves movies from IMDBs.  You can either specify a full URL or add a search flag and it will retrieve the top google result.

If used with the --intact and --save flag, this is actually a very easy way to download scripts rapidly.  

However, it can also perform manipulation and analysis on the scripts such as alphabetizing the words (highly useful) or providing word frequency.

## Why?

Why not?

## Usage

```
usage:  python [optional flags] -movie movie/url
	--h/help  display argument options
	--search  optional flag that indicates you want to search and the program 
			  will return the top movie hit.  results not guaranteed.

	--intact  optional flag that will actually just retrieve a script for you
			  without performing any input.  this will print the script as
			  written by the writer and render and further commands irrelevant
			  as they rely on eliminating whitespace.  this can be used with 
			  the --save flag to produce {movie}_intact_script.txt

	--save    optional flag that will save the output to directory with a file
	 		  name {movie}_{command}.txt
	
	--reverse optional flag that will reverse the command output.

	--command optional but reccomended command to peform.  see the wordanalyzer 
	          class for a list of options.  default is to return an alphabetized 
			  list.  this command supports multiple sequential arguments.

	--movie   [required] the movie to return.  
```

