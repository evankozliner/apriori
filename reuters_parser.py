""" Simple parser for the reuters data, shamlessly taken from
    https://www.quantstart.com/articles/Supervised-Learning-for-Document-Classification-with-Scikit-Learn
"""

import re
from HTMLParser import HTMLParser

class ReutersParser(HTMLParser):
    def __init__(self, encoding='latin-1'):
        HTMLParser.__init__(self)
        self._reset()
        self.encoding = encoding

    def _reset(self):
        self.in_body = False
        self.in_topics = False
        self.in_topic_d = False
        self.in_places = False
        self.in_places_d = False
        self.body = ""
        self.topics = []
        self.places = []
        self.topic_d = ""
        self.places_d = ""

    def parse(self, fd):
        self.docs = []
        for chunk in fd:
            self.feed(chunk.decode(self.encoding))
            for doc in self.docs:
                yield doc
            self.docs = []
        self.close()

    def handle_starttag(self, tag, attrs):
        if tag == "reuters":
            pass
        elif tag == "body":
            self.in_body = True
        elif tag == "topics":
            self.in_topics = True
        elif tag == "places":
            self.in_places = True
        elif tag == "d" and self.in_topics:
            self.in_topic_d = True 
        elif tag == "d" and self.in_places:
            self.in_places_d = True 

    def handle_endtag(self, tag):
        if tag == "reuters":
            self.body = re.sub(r'\s+', r' ', self.body)
            self.docs.append( (self.topics, self.places, self.body) )
            self._reset()
        elif tag == "body":
            self.in_body = False
        elif tag == "places":
            self.in_places = False
        elif tag == "topics":
            self.in_topics = False
        elif tag == "d" and self.in_topics:
            self.in_topic_d = False
            self.topics.append(self.topic_d)
            self.topic_d = ""  
        elif tag == "d" and self.in_places:
            self.in_places_d = False
            self.places.append(self.places_d)
            self.places_d = ""  

    def handle_data(self, data):
        if self.in_body:
            self.body += data
        elif self.in_topic_d:
            self.topic_d += data
        elif self.in_places_d:
            self.places_d += data


