from flask import Flask
from anagram.dao.anagram_dao import AnagramDao

import configparser

from anagram.service.anagram_service import AnagramService

config = configparser.ConfigParser()
config.read('config.ini')

app = Flask(__name__)
# Connect to database
db = AnagramDao(config.get('DEFAULTS', 'connection_url'))

# Init service
anagramService = AnagramService("")
# API definitions
