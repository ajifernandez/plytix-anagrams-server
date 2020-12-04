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
        self.anagrams = self.calculate_anagrams(self.db.get_words_db())

    def get_words(self) -> list:
        logging.info("[anagram_service]Getting words")
        return self.db.get_words()

    def save_words(self, words: list) -> bool:
        logging.info("[anagram_service]Saving words")
        return self.db.fill_database(words)

    def get_anagrams(self, word: str) -> list:
        logging.info("[anagram_service]Getting anagrams")
        sorted_word = ''.join(sorted(word))
        return self.anagrams.get(sorted_word, '-')

    @staticmethod
    def calculate_anagrams(words: list) -> dict:
        """
        Calculate the anagrams of the words list sorting every letter word and setting it as key
        :param words: list of words
        :return: dict with the anagrams
        """
        logging.info("[anagram_service]Generating dict of anagrams words")
        d = defaultdict(list)
        for word in words:
            key = ''.join(sorted(word))  # frase -> aefrs
            d[key].append(word)
        return d
