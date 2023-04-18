from bottle import get, post, request, response,  run # or route
from GoogleTranslator import GoogleTranslator

class RequestsHandler(GoogleTranslator):
    def __init__(self, Unset = False, to_lang = None) -> None:
        self.translator = GoogleTranslator()
        self.Unset = Unset
        self.to_lang = to_lang

    def get_languages_list(self) -> list:
        try:
            output_json = {'error' : False, 'languages' : self.translator.get_languages_list()}
            response.status = 200
        except:
            output_json = {'error' : True, 'languages' : 'Unhandled exception'}
            response.status = 500
        return output_json
    def translate(self, input_json) -> str:
        try:
            input_json = input_json
            if input_json == {}:
                raise KeyError("Excpected json as input")
            if self._check_word_of_sentence(input_json['text']) == True:
                raise ValueError('Unsupported value format')
            if self._check_lang(input_json['to_lang']) == False and self.to_lang == None:
                raise ValueError('Unsupported value format')
            
            for _ in input_json:
                if input_json['text'] and self._check_lang(input_json['to_lang']) and self.to_lang == None:
                    output_json = {"error" : False, "result" : str(self.translator.translate(input_json['text'],to_lang=input_json['to_lang']))}
                if input_json['text'] and self.to_lang != None:
                    output_json = {'error' : False, 'result' : str(self.translator.translate(input_json['text'],to_lang=translator.to_lang))}
                if input_json['text'] and self.to_lang != None and self._check_lang(input_json['to_lang']):
                    output_json = {"error" : False, "result" : str(self.translator.translate(input_json['text'],to_lang=input_json['to_lang']))}
                return output_json
    
        except KeyError:
            output_json = {'error' : True,
                'description' : 'Excpected json as input'}
            response.status = 400
            return output_json
        
        except ValueError:
            output_json = {'error' : True,
                'description' : 'Unsupported value format'}
            response.status = 400
            return output_json
        
        except :
            output_json = {'error' : True,
                'description' : 'Unhandled exception'}
            response.status = 500
            return output_json
    def post_default_language(self, input_json):
        try:
            if input_json == {}:
                raise KeyError("Excpected json as input")
        
            if input_json['Unset'] == True:
                    self.Unset = False
                    self.to_lang = None
                    output_json = {'error' : False}
                    return output_json

            if self._check_lang(input_json['lang']) == True:
                for _ in input_json:
                    if input_json['Unset'] == False:
                        self.Unset = True
                        self.to_lang = input_json['lang']
                        output_json = {'error' : False}
                    return output_json       
            else:
                output_json = {'error' : True,
                'description' : 'Unsupported language format'}
                response.status = 400
                return output_json

        except KeyError:
            output_json = {'error' : True,
               'description' : "Excpected json as input"}
            response.status = 400
            return output_json

        except ValueError:
            output_json = {'error' : True,
               'description' : 'Unsupported value format'}
            response.status = 400
            return output_json

        except :
            output_json = {'error' : True,
            'description' : 'Unhandled exception'}
            response.status = 500 
            return output_json
    def default_language(self):
        try:
            if self.Unset and self.to_lang:
                output_json = {'error' : False, 'lang' : self.to_lang}
                return output_json
            else:
                output_json = {'error' : False, 'lang' : None}
            return output_json
        except :
            output_json = {'error' : True, 'description' : 'Unhandled exception'} 
            response.status = 500
            return output_json

    def _check_lang(self, lang):
        if lang =="":
            return False
        else:
            for elem in self.translator.get_languages_list():
                if lang == elem:
                    return True
            return False
    def _check_word_of_sentence(self, text):
        if text == "":
            return False
        else:
            update = text.split()
            for elem in update:
                for i in range(len(elem)-1):
                    if elem[i].isalpha() and elem[i+1].isnumeric() or elem[i+1].isalpha() and elem[i].isnumeric():
                        return True
            return False

translator = RequestsHandler()
@get('/api/v1/available_languages')
def handler():
    return translator.get_languages_list()

@post('/api/v1/translate')
def handler():
    return translator.translate(request.json)

@post('/api/v1/default_language')
def handler():
    return translator.post_default_language(request.json)

@get('/api/v1/default_language')
def handler():
    return translator.default_language()
run(host='92.118.114.138', port=8080)
