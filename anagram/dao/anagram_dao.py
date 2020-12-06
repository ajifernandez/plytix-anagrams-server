from pymongo import MongoClient, errors
from pymongo.errors import ServerSelectionTimeoutError
from app_exception import AppException, GenericErrorMessages
import logging


class AnagramDao:

    def __init__(self, connection_url: str) -> None:
        """
        Constructor of AnagramDao with the connection url
        :param connection_url: url of database connection
        """
        logging.info("[anagram_dao]Creating AnagramDao")
        self.connection_url = connection_url
        self.schema = connection_url.split('/')[-1]
        logging.info("[anagram_dao]connection_url " + self.connection_url)
        logging.info("[anagram_dao]schema " + self.schema)
        try:
            # Connect with mongodb
            self.connection = self.open_connection()

            # Get database from URL connection
            self.db = self.connection.get_database()

            # Get collection. Create if not exist
            if self.schema not in self.db.collection_names():
                self.db.create_collection(self.schema)
            self.mongo_collect = self.db[self.schema]
        except errors.ConfigurationError:
            logging.error("[anagram_dao]CONFIGURATION_ERROR")
            raise AppException(GenericErrorMessages.CONFIGURATION_ERROR)
        except AppException as e:
            logging.error("[anagram_dao]"+str(e))
            raise e

    def open_connection(self) -> MongoClient:
        """
        Open the connection with the database.
        :return: connection object
        :rtype: object
        """
        logging.info("[anagram_dao]Open the database connection")
        try:
            connection = MongoClient(self.connection_url)
            connection.is_mongos
        except (errors.ConnectionFailure, errors.ServerSelectionTimeoutError):
            raise AppException(GenericErrorMessages.DATABASE_ERROR)
        logging.info("[anagram_dao]Connection opened")
        return connection

    def get_anagram(self, word: str) -> list:
        """
        Retrieve the words that fit with the key
        :return: words
        """
        logging.info("[anagram_dao]getting words of anagram " + word)
        try:
            result = []
            for o in list(self.mongo_collect.find({"anagram": {'$eq': word}})):
                result.append(o["word"])
            return result
        except ServerSelectionTimeoutError:
            raise AppException(GenericErrorMessages.DATABASE_ERROR)

    def get_words(self) -> list:
        """
        Retrieve all the words from database
        :return: words
        """
        logging.info("[anagram_dao]getting all the words")
        try:
            result = []
            for o in list(self.mongo_collect.find({}, {'word': 1})):
                result.append(o["word"])
            return result
        except ServerSelectionTimeoutError:
            raise AppException(GenericErrorMessages.DATABASE_ERROR)

    def save_words(self, data: dict) -> bool:
        """
        Save the data into database. First drop and then insert
        :param data: data to insert
        :return: bool
        """
        logging.info("[anagram_dao]saving words and anagrams")
        try:
            self.mongo_collect.drop()
            for key in data:  # where the key is the natural word
                self.mongo_collect.insert({'word': key, 'anagram': data[key]})
        except ServerSelectionTimeoutError:
            raise AppException(GenericErrorMessages.DATABASE_ERROR)
        return True
