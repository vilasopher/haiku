# haiku.py
# goal: to create a haiku out of randomly input words
# author: Vilas Winstein

########################################################
# FUNCTIONS TO COUNT THE NUMBER OF SYLLABLES IN A WORD #
########################################################

import cmudict
d = cmudict.dict()

# count the number of syllables using CMUdict
# copied from a stack exchange post
def syllables(word):
    try:
        return [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]][0]
    except IndexError:
        # if word not found in cmudict
        return weak_syllables(word)

# a fail-safe version of the syllable counter to use if a word is not in CMUdict
#referred from stackoverflow.com/questions/14541303/count-the-number-of-syllables-in-a-word
def weak_syllables(word):
    count = 0
    vowels = 'aeiouy'
    word = word.lower()
    if word[0] in vowels:
        count +=1
    for index in range(1,len(word)):
        if word[index] in vowels and word[index-1] not in vowels:
            count +=1
    if word.endswith('e'):
        count -= 1
    if word.endswith('le'):
        count += 1
    if count == 0:
        count += 1
    return count

############################################################################
# FUNCTIONS TO GENERATE A RANDOM HAIKU GIVEN A STRING OF MANY SOURCE WORDS #
############################################################################

import random

# pick a word at random from a list of words
# with an upper bound on the number of syllables in the chosen word
# returns None if no satisfactory word was found
def random_word(wordlist, maxsyllables, maxtriesperword=1000):
    word = random.choice(wordlist)
    trycounter = 0

    while(syllables(word) > maxsyllables and trycounter < maxtriesperword):
        word = random.choice(wordlist)
        trycounter = trycounter + 1

    if trycounter < maxtriesperword:
        return word
    else:
        return None

# generate a line with a given number of syllables.
def random_line(wordlist, numsyllables, maxtriesperline=1000, maxtriesperword=1000):
    line = []
    currentsyllables = 0
    trycounter = 0

    while currentsyllables < numsyllables and trycounter < maxtriesperline:
        word = random_word(wordlist, numsyllables - currentsyllables, maxtriesperword=maxtriesperword)

        if word == None:
            line = []
            currentsyllables = 0
            trycounter = trycounter + 1
        else:
            line.append(word)
            currentsyllables = currentsyllables + syllables(word)

    if trycounter < maxtriesperline:
        return ' '.join(line)
    else:
        return None

# generate a random haiku
def random_haiku(wordlist, shape=[5,7,5], maxtriesperline=1000, maxtriesperword=1000):
    lines = []

    for i in range(len(shape)):
        lines.append(random_line(wordlist, shape[i], maxtriesperline=maxtriesperline, maxtriesperword=maxtriesperword))

    if None in lines:
        print('Sorry, a haiku could not be generated in time.')
    else:
        return lines


#################################
# FUNCTIONS FOR PRINTING HAIKUS #
#################################

import re

# regex for removing non alphabetical characters
regex = re.compile('[^a-zA-Z ]')

# pad a haiku line
def padded(line, length):
    spacesbefore =int((length - len(line))/2)
    return ' ' * spacesbefore + line

# print a haiku
# a haiku is a list of lists of words
def print_haiku(haiku):
    max_characters = max([len(s) for s in haiku])

    for line in haiku:
        print(padded(line, max_characters))

# print a haiku from a file
def print_haiku_from_file(fname, shape=[5,7,5], maxtriesperline=1000, maxtriesperword=1000):
    fo = open(fname)
    wordlist = regex.sub('', fo.read()).split()
    haiku = random_haiku(wordlist, shape=shape, maxtriesperline=maxtriesperline, maxtriesperword=maxtriesperword)
    print_haiku(haiku)


########################################
# WHEN THIS FILE IS RUN AS A SCRIPT... #
########################################

import sys
import ast

def is_list_of_positive_integers(a):
    if type(a) != list:
        return False
    else:
        return False not in [ type(x) == int and x > 0 for x in a ]

def is_pos_int(a):
    return type(a) == int and a > 0

# dictionary containing the possible arguments for this program,
# and functions to check the arguments to the arguments.
possible_args = {
    '-shape' : (is_list_of_positive_integers, 'a list of positive integers') , 
    '-linetries' : (is_pos_int, 'a positive integer') , 
    '-wordtries' : (is_pos_int, 'a positive integer')
}

def print_help_message():
    print('haiku.py is a program that creates a random haiku out of the words in any text file')
    print('typical usage:')
    print('')
    print('\tpython haiku.py words.txt')
    print('')
    print('options:')
    print('')
    print('\t-shape        is the shape of the haiku')
    print('\t              default is -shape [5,7,5]')
    print('')
    print('\t-linetries    is the number of invalid lines before haiku.py gives up')
    print('\t              default is -linetries 1000')
    print('')
    print('\t-wordtries    is the number of invalid words before haiku.py gives up')
    print('\t              default is -wordtries 1000')
    print('')
    print('\t-help         prints this dialog')

# main code block
if __name__ == '__main__':
    arguments = sys.argv[1:]

    arg_dict = {
        'shape' : [5,7,5], 
        '-linetries' : 1000,
        '-wordtries' : 1000
    }

    arguments_lower = [ x.lower() for x in arguments ] 

    if '-help' in arguments_lower or 'help' in arguments_lower or '--help' in arguments_lower:
        print_help_message()
        sys.exit()

    for arg in possible_args:
        if arg in arguments:
            index = arguments.index(arg)
            del arguments[index]

            if index >= len(arguments):
                print('Error: no argument given for', arg)
                sys.exit()

            try:
                arg_dict[arg] = ast.literal_eval(arguments[index])
            except:
                print('Error: couldn\'t parse argument to', arg)
                sys.exit()

            del arguments[index]
            
            if not possible_args[arg][0](arg_dict[arg]):
                print('Error:', arg, 'argument,', arg_dict[arg], ', is not', possible_args[arg][1])
                sys.exit()

    if len(arguments) > 1:
        print('Error: extraneous arguments given.')
        sys.exit()

    filename = arguments[0]

    print_haiku_from_file(filename, shape=arg_dict['shape'], maxtriesperline=arg_dict['-linetries'], maxtriesperword=arg_dict['-wordtries'])
