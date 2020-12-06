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

    def get_words(self) -> list:
        logging.info("[anagram_service]Getting words")
        return self.db.get_words()

    def save_words(self, words: list) -> bool:
        """
        Save the word list after calculate every anagram
        :param words: list of word
        :return: true if persist the data
        """
        logging.info("[anagram_service]Saving words")
        return self.db.save_words(self.calculate_anagrams(words))

    def get_anagrams(self, word: str) -> list:
        logging.info("[anagram_service]Getting anagrams")
        sorted_word = ''.join(sorted(word))
        return self.db.get_anagram(sorted_word)

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
            key = ''.join(sorted(word))
            d[word].append(key)
        return d
