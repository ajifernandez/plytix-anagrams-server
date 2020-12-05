from pymongo import MongoClient, errors
from pymongo.errors import ServerSelectionTimeoutError
from app_exception import AppException, GenericErrorMessages
import logging
logging.basicConfig(level=logging.INFO)


class AnagramDao:

    def __init__(self, connection_url: str) -> None:
        """
        Constructor of AnagramDao with the connection url
        :param connection_url: url of database connection
        """
        self.connection_url = connection_url
        self.schema = connection_url.split('/')[-1]

        try:
            # Connect with mongodb
            self.connection = self.open_connection()

            # Get database from URL connection
            self.db = self.connection.get_database()

            # Get collection. Create if not exist
            if self.schema not in self.db.collection_names():
                self.db.create_collection(self.schema)
            self.mongo_collect = self.db[self.schema]
            # self.mongo_collect.drop()
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

        try:
            connection = MongoClient(self.connection_url)
            connection.is_mongos
            return connection

        except (errors.ConnectionFailure, errors.ServerSelectionTimeoutError):
            raise AppException(GenericErrorMessages.DATABASE_ERROR)

    def get_anagram(self, word: str) -> list:
        """
        Retrieve the words that fit with the key
        :return: words
        """

        try:
            result = []
            for o in list(self.mongo_collect.find({"anagram": {'$eq': word}})):
                for word in o["words"]:
                    result.append(word)
            return result
        except ServerSelectionTimeoutError:
            raise AppException(GenericErrorMessages.DATABASE_ERROR)

    def get_words(self) -> list:
        """
        Retrieve all the words from database
        :return: words
        """

        try:
            result = []
            for o in list(self.mongo_collect.find({}, {'words': 1})):
                for word in o["words"]:
                    result.append(word)
            return result
        except ServerSelectionTimeoutError:
            raise AppException(GenericErrorMessages.DATABASE_ERROR)

    def fill_database(self, data: dict) -> bool:
        """
        Fill the database with the list data. First drop and then insert
        :param data: data to insert
        :return: bool
        """
        try:
            self.mongo_collect.drop()
            for key in data:
                self.mongo_collect.insert({'anagram': key, 'words': data[key]})
            # self.mongo_collect.insert(data)
        except ServerSelectionTimeoutError:
            raise AppException(GenericErrorMessages.DATABASE_ERROR)
        return True
