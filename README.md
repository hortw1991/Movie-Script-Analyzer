# Movie-Script-Analyzer

## What?

This script retrieves movies from IMDBs.  You can either specify a full URL or add a search flag and it will retrieve the top google result.

If used with the --intact and --save flag, this is actually a very easy way to download scripts rapidly.  

However, it can also perform manipulation and analysis on the scripts such as alphabetizing the words (highly useful) or providing word frequency.

## Why?

Why not?

## Usage

```
python [optional flags] -m movie/url

	--search  Optional flag that indicates you want to search and the program 
			  will return the top movie hit.  Results not guaranteed.
	--intact  Optional flag that will actually just retrieve a script for you
			  without dummifying it.  This will not invoke any 
	--save    Optional flag that will save the output to a file.
	--movie   [REQUIRED] The movie to return.
```

