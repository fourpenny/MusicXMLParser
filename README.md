# MusicXMLParser

A MusicXML Parser made in Python! Simply pass in each .musicxml file as an argument to the "parse_score()" function and call one of the retrieval methods, .get_dict() or .get_json(), on the Score object it creates. You can also use the "parse_many_scores()" function to get a dictionary of Score objects if you would like to retrieve data from multiple scores at once.

## Install
Download the "mxml_parser.py" file from this repo, then add it to your project directory. You should be able to use it as a module by including "import mxml_parser" at the top of the Python script you would like to use it in.

## Features
The Score object stores the following data which can be retrieved using the either the .get_json() or .get_dict() method:
- The work's title
- The work's composer
- The work's instruments
- The number of occurances of each pitch class

Feel free to make a pull request if you would like to contribute any new features!
