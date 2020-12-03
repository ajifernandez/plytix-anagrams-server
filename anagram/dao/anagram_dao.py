from pymongo import MongoClient, errors

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
