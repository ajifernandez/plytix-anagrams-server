from flask import Flask, Response, jsonify, request
from flask_cors import CORS
from app_exception import AppException
from anagram.dao.anagram_dao import AnagramDao
from anagram.service.anagram_service import AnagramService
import configparser
import logging
logging.basicConfig(level=logging.INFO)

# Configuration reader/parser of config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

# Flask
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# Instantiate and Connect to database
db = AnagramDao(config.get('DEFAULTS', 'connection_url'))

# Init service
anagramService = AnagramService(db)


@app.route('/api/anagrams/fill')
def fill_database():
    """
    Fill database with data test
    :return: 200 ok or exception
    """
    logging.info("[api]Filling database")

    try:
        data = ['riesgo', 'roma', 'mora', 'frase', 'paris']
        anagramService.fill_database(data)
        return Response(status=200)
    except AppException as e:
        logging.error("[api]"+str(e))


@app.route('/api/anagrams/words')
def get_words():
    """
    Retrieve the words from database
    :return: json with the words or exception
    """
    logging.info("[api]Getting words")

    try:
        return jsonify(anagramService.get_words())
    except AppException as e:
        logging.error("[api]"+str(e))


@app.route('/api/anagrams/save', methods=['POST'])
def save():
    """
    Save the words into the database
    :return: 200 ok or exception
    """

    try:
        data = request.json
        if anagramService.save_words(data):
            return Response(status=200)
        else:
            return Response(status=500)
    except AppException as e:
        logging.error("[api]"+str(e))


@app.route('/api/anagrams/anagrams', methods=['POST'])
def get_anagrams():
    """
    Get anagrams that fit with the searched string
    :return: 200 ok or exception
    """

    try:
        data = request.data.decode('utf-8')
        return jsonify(anagramService.get_anagrams(data))
    except AppException as e:
        logging.error("[api]"+str(e))
        

if __name__ == '__main__':
    app.run()
