from Translator import Translator
from googletrans import Translator as trans
from googletrans.constants import LANGCODES

class GoogleTranslator(Translator):
    def translate(self, text: str,from_lang = 'auto', to_lang =  str) -> str:
        translator = trans()
        translation = translator.translate(text=text, src=from_lang, dest = to_lang)
        return translation.text
    
    def get_languages_list(self) -> dict:
        return LANGCODES
