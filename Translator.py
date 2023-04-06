from abc import ABCMeta, abstractmethod


class Translator(metaclass=ABCMeta):
    @abstractmethod
    def translate(self,text : str, to_lang : str) -> str:
        pass
        
    @abstractmethod
    def get_languages_list(self) -> list:
        pass

