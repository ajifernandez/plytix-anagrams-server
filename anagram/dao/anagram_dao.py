from pymongo import MongoClient, errors
from pymongo.errors import ServerSelectionTimeoutError

from app_exception import AppException, GenericErrorMessages


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

        except errors.ConfigurationError:
            raise AppException(GenericErrorMessages.CONFIGURATION_ERROR)
        except AppException as e:
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

    def get_words_db(self) -> list:
        """
        Get words from database
        :return: words from database
        """

        output = list()
        db_words = self.get_words()

        for db_word in db_words:
            output.append(db_word['word'])

        return output

    def get_words(self) -> list:
        """
        Retrieve all the words from database
        :return: words
        """

        try:
            return list(self.mongo_collect.find({}, {'_id': False}))
        except ServerSelectionTimeoutError:
            raise AppException(GenericErrorMessages.DATABASE_ERROR)

    def fill_database(self, data: list) -> bool:
        """
        Fill the database with the list data. First drop and then insert
        :param data: data to insert
        :return: bool
        """
        self.mongo_collect.drop()
        self.mongo_collect.insert(data)
        return True
