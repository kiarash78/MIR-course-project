import xml.etree.ElementTree as ET
import re
from collections import Counter
import numpy as np
from hazm import Normalizer, word_tokenize, Stemmer
from helper import Tf_calc, Text_cleaner

class Doc:

    PARTS = ('text', 'title')

    def __init__(self, doc_id=None, title=None, text=None, original_words=None):
        self.doc_id = doc_id
        self.title = title
        self.text = text
        self.original_words = original_words
        self._bag_of_words = {'text':None, 'title':None, 'all':None}

    @classmethod
    def create_from_xml(cls, xml, method='file'):

        root = Doc.get_root(xml, method)
        doc_id = root[2].text
        cleaned_title = Doc.extract_clean_title(root)
        cleaned_text = Doc.extract_clean_text(root)
        prepared_title = Text_cleaner.prepare_text(cleaned_title)
        prepared_text = Text_cleaner.prepare_text(cleaned_text)
        return cls(doc_id, prepared_title, prepared_text)

    @classmethod
    def from_query(cls, title, text):
        
        doc_id = -1
        title = Text_cleaner.clean_and_prepare_text(title)
        text = Text_cleaner.clean_and_prepare_text(text)
        return cls(doc_id, title, text)

    @staticmethod
    def get_field_number(root, name):
        for i, field in enumerate(root):
            if name in field.tag:
                return i
        return -1

    @staticmethod
    def extract_clean_title(root):
        i = Doc.get_field_number(root, 'title')
        if i == -1:
            print(1)
            return ''
        return Text_cleaner.clean_text(root[i].text)

    @staticmethod
    def extract_clean_text(root):
        i = Doc.get_field_number(root, 'revision')
        if i == -1:
            print(2)
            return ''
        root = root[i]

        i = Doc.get_field_number(root, 'text')
        if i == -1:
            print(3)
            return ''
        return Text_cleaner.clean_text(root[i].text)

    @classmethod
    def create_list_from_xml(cls, xml, max_num=None, method='file'):

        root = Doc.get_root(xml, method)
        li = []
        for i, doc_root in enumerate(root):
            if max_num is not None and i >= max_num:
                break
            li.append(cls.create_from_xml(doc_root, method='root'))
        return li

    @staticmethod
    def get_root(xml, method):
        if method == 'root':
            return xml
        if method == 'file':
            tree = ET.parse(xml)
            return tree.getroot()
        raise ValueError("Method %s is not supported" % method)

    def bag_of_words(self, part='text'):
        if self._bag_of_words[part] is None:
            self._bag_of_words[part] = Counter(self.get_part_iterator(part))
        return self._bag_of_words[part]
    
    def get_part_iterator(self, part):
        put_title = part in ['title', 'all']
        put_text = part in ['text', 'all']
        if put_title:
            for word in self.title:
                yield word

        if put_text:
            for word in self.text:
                yield word

    def distinct_terms(self, part='text'):
        return self.bag_of_words(part).keys()
        
    @property
    def info_iterator(self):
        """returns word_pos_part"""
        for i, word in enumerate(self.title):
            yield (word, i + 1, 'title')

        for i, word in enumerate(self.text):
            yield (word, i + 1, 'text')

    def tf_idf(self, method):

        if method[1] != 'n':
            raise ValueError("IDF not supported")

        v = dict()
        const = dict()
        for part in Doc.PARTS:
            v[part] = dict()
            for word, count in self.bag_of_words(part).items():
                v[part][word] = Tf_calc.transform_tf(count, method[0]) 
    
            const[part] = Tf_calc.const(v, method[2])
        return v, const

    def __repr__(self):
        return str(self).replace("\n", "\\n").replace("\t", "\\t")

    def __str__(self):
        ans = ""
        ans += "ID: %s\n" % self.doc_id
        ans += "Title: %s\n\n" % ' '.join(self.title)
        ans += ' '.join(self.text)
        return ans
    
