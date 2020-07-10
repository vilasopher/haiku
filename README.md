# haiku

haiku.py is a program that creates a random haiku out of the words in any text file

typical usage:

	python haiku.py words.txt

options:

	-shape        is the shape of the haiku
	              default is -shape [5,7,5]

	-linetries    is the number of invalid lines before haiku.py gives up
	              default is -linetries 1000

	-wordtries    is the number of invalid words before haiku.py gives up
	              default is -wordtries 1000

	-help         prints this dialog

this program depends on the CMUDict python library
