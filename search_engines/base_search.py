# search_engines/base_search.py
from abc import ABC, abstractmethod

class BaseSearch(ABC):
    @abstractmethod
    def search(self, query: str):
        pass
