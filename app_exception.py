import logging


class AppException(Exception):
    """
    Standard exception of the application
    """

    def __init__(self, msg: str = '') -> None:
        """
        Constructor with optional message
        :param msg: optional message of the exception
        :type msg: str
        :return: This function return nothing
        :rtype: None
        """
        Exception.__init__(self, msg)


class GenericErrorMessages:
    """
    Generic Errors Messages for all the application
    """

    # Error messages
    CONFIGURATION_ERROR = 'Configuration error in config.ini'
    DATABASE_ERROR = 'Database connection error'
