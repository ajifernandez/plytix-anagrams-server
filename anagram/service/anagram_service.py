from collections import defaultdict

from anagram.dao.anagram_dao import AnagramDao

class AnagramService:

    def __init__(self, db: AnagramDao):
        self.db = db
        self.anagrams = self.calculate_anagrams(db.get_words_db())

    @staticmethod
    def fill_database(self, words: list) -> None:
        self.db.fill_database(words)

    @staticmethod
    def calculate_anagrams(words: list) -> dict:
        d = defaultdict(list)
        return d
