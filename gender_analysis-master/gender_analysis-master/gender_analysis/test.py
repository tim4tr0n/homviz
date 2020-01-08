# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 20:00:00 2020

@author: 17025
"""

#from gender_analysis import document
#from pathlib import Path
#from gender_analysis import common
import gender_analysis

document_metadata = {'author': 'Austen, Jane', 'title': 'Persuasion', 'date': '1818',
                      'filename': 'austen_persuasion.txt', 'filepath': Path(common.TEST_DATA_PATH, 'sample_novels', 'texts', 'austen_persuasion.txt')}
austen = document.Document(document_metadata)
print(type(austen.text))