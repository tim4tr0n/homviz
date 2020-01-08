# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 22:03:47 2020

@author: 17025
"""
# https://gender-analysis.readthedocs.io/en/latest/tutorial/tutorial.html
# Might be easiest just to give this page on the docs a quick read-through, tells you all the basics of the Document and Corpus classes

import time

from corpus import * # This is the main file that we'll be using for the analysis; for our purposes, it's essentially a convenient
                     # wrapper to store and step through Documents, each of which contains text, metadata, and some built-in methods, i.e. doc.get_word_freq()
                     
from pathlib import Path # Pretty sure this just allows you to create a path separated by commas instead of slashes. Could be useful.

class Homunculus:
    def __init__(self):
        self._body_dict = {'arms':0, 'legs':0, 'lips':0} # etc. However y'all decide to split up the body parts, you can specify that in the intialized dict

    def get_body_dict_count(self, part):
        try:
            return self._body_dict[part]
        except KeyError:
            raise InvalidBodyPartError
            
    def set_body_dict_count(self, part, count):
        try:
            self._body_dict[part] = count
        except KeyError:
            raise InvalidBodyPartError # Way I envision it, we preload all dict entries so this error should never raise if done properly.
            
    def add_body_dict_count(self, part, inc):
        try:
            self._body_dict[part] += inc
        except KeyError:
            raise InvalidBodyPartError

class InvalidBodyPartError(Exception):
    def __init__(self):
        pass

arm_words = ['arms','arms','armed','arming']
leg_words = ['legs','leg','legged','leggings']
# etc.
    
#document_metadata = {'author': 'Austen, Jane', 'title': 'Persuasion', 'date': '1818',
#                     'filename': 'austen_persuasion.txt', 'filepath': Path(TEST_DATA_PATH, 'sample_novels', 'texts', 'austen_persuasion.txt')}
# All documents are initialized with metadata in the form of a dict such as the one above. However, putting
# all the .txt files into a folder will allow you to create a Corpus object, which will automate all that
# shit; you just have to make a .csv file in the same directory with the top rows as fields, e.g. 'author, title, date_created',
# all separated by commas, and then everything below it is the values starting with the first .txt file, all separated by 
# commas in the same order. 

##############################################################################
#austen = Document(document_metadata)
#print(type(austen.text))
#print(len(austen.text))
#
#print(austen.get_word_freq('she'))

####This was just me testing the functionality of Document directly above.####

path = TEST_DATA_PATH / 'sample_novels' / 'texts'
c = Corpus(path)
print(type(c.documents), len(c))
h = Homunculus()

 #etc. again, I suppose you'll have to do all the variations, e.g. 'arms','armed','arming',etc.
for doc in c.documents:
    
    
    ####################################69############################################################
        # My really simplistic algorithm for counting up simple nouns in each doc within the test corpus.
        
    #    tag_list = doc.get_part_of_speech_tags() # Really simple way to tag every word in a doc with part of speech using NLTK. But slow as FUCK lol
    #    for term, tag in tag_list:
    #        if tag == 'NN': # Different parts of speech have different tags, and there is a LOT of nuance. Check this site out to learn more: https://www.nltk.org/book/ch05.html
    #            hits += 1
    #    print(hits)
        
    ##############420#######################################1337######################################
    for part_type in (arm_words, leg_words):
        part_name = part_type[0]
        total_part_hits = 0
        
        for term in part_type:
            start_time = time.perf_counter()
            
            term_hits = doc.get_count_of_word(term)
            total_part_hits += term_hits 
                                     # My advice would be to systematically go through the list of body parts that we agree on
                                     # and then for each one, check all the related words, e.g. 'arm','arms','armed','arming',etc.
                                     # What's nice is that you only need to get the word counts of any doc once, and then there's a dict
                                     # stored in the Document instance that maps all words to their count.
#            print(doc.word_count)
            print(total_part_hits)
            print("--- %s seconds ---" % (time.perf_counter() - start_time))
    
        h.add_body_dict_count(part_name, total_part_hits)
