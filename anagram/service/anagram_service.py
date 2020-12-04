from collections import defaultdict

from anagram.dao.anagram_dao import AnagramDao
import logging
logging.basicConfig(level=logging.INFO)


class AnagramService:
    """
    Service for Anagrams
    """

    def __init__(self, db: AnagramDao):
        """
        Constructor with db as param
        :param db: dao of Anagram
        """
        self.db = db
        self.anagrams = self.calculate_anagrams(db.get_words_db())

    def fill_database(self, words: list) -> None:
        logging.info("[anagram_service]Filling database")
        self.db.fill_database(words)

    def get_words(self) -> list:
        logging.info("[anagram_service]Getting words")
        return self.db.get_words()

    @staticmethod
    def calculate_anagrams(words: list) -> dict:
        d = defaultdict(list)
        return d
