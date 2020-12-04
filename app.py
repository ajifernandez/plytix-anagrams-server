from flask import Flask, Response
from anagram.dao.anagram_dao import AnagramDao

import configparser

from anagram.service.anagram_service import AnagramService
from app_exception import AppException

# Configuration reader/parser of config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

# Flask
app = Flask(__name__)

# Instantiate and Connect to database
db = AnagramDao(config.get('DEFAULTS', 'connection_url'))

# Init service
anagramService = AnagramService(db)


@app.route('/api/fill')
def fill_database():
    """
    Fill database with data test
    :return: 200 ok or exception
    """

    try:
        data = [{'word': 'riesgo'}, {'word': 'roma'}, {'word': 'frase'}, {'word': 'roma'}, {'word': 'paris'}]
        anagramService.fill_database(data)
        return Response(status=200)
    except AppException as e:
        print(e)


if __name__ == '__main__':
    app.run()
