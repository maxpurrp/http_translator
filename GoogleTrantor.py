from Translator import Translator
from googletrans import Translator as trans
from googletrans.constants import LANGCODES

class GoogleTranslator(Translator):
    def translate(self, text: str,from_lang = 'auto', to_lang =  str) -> str:
        translator = trans()
        translation = translator.translate(text=text, src=from_lang, dest = to_lang)
        return translation.text
    
    def get_languages_list(self) -> list:
        lang_list = []
        for value in  LANGCODES.values():
            lang_list.append(value)
        return lang_list
