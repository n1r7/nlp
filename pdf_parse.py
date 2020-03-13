# IMPORTS

import sys
import io
import functools
import timeit

from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage

import re

from nltk import tokenize

import pandas as pd



# DEFINE FUNCTION TO PARSE PDF TEXT TO STRING

def extract_text(pdf_path):
    content = []
    
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
 
    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh, 
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)
 
        text = fake_file_handle.getvalue()
 
    # close open handles
    converter.close()
    fake_file_handle.close()
 
    if text:
        return text

    content.append(text)



# DEFINE FUNCTION TO PARSE STRING TO SENTENCES

@functools.lru_cache(maxsize=128)
def sentence_tokenizer(content):
    sents = tokenize.sent_tokenize(content)
    return sents


# START PARSE

path = 'Private_equity.pdf'

pdf = extract_text(path)

pdf = re.sub('\x0c \d\d\d', '', pdf)

pdf = pdf.replace('\uf0d8', '')

pd.set_option('display.max_colwidth',0)

df = pd.DataFrame(data=sentences)

df.head(20)
