from bottle import get, post, request, response,  run # or route
from GoogleTranslator import GoogleTranslator

localhost, port = '92.118.114.138', 8080
class RequestsHandler():
    def __init__(self, unset = False, to_lang = None) -> None:
        self.translator = GoogleTranslator()
        self.unset = unset
        self.to_lang = to_lang

    def get_languages_list(self) -> list:
        return self.translator.get_languages_list()
    def translate(self, input_json) -> str:
        if input_json == None:
            raise TypeError('Expected json')
        if 'text' not in input_json or 'to_lang' not in input_json:
            raise KeyError('Expected text and to_lang in json')
        if self._check_lang(input_json['to_lang']) == False and self.to_lang == None:
            raise ValueError('Invalid language')
        cur_lang = input_json['to_lang']
        if cur_lang == '':
            cur_lang = self.to_lang
        result = self.translator.translate(input_json['text'],to_lang=cur_lang)
        return result
    def save_default_language(self, input_json) -> bool:
            if input_json == None:
                raise TypeError('Expected json')
            if 'unset' not in input_json:
                raise KeyError('Expected unset in json')
            if self._check_lang(input_json['lang']) == False:
                 raise ValueError('Unvalid language')
            
            if input_json['unset'] == True:
                    self.unset = False
                    self.to_lang = None
                    errors = False

            if self._check_lang(input_json['lang']) == True:
                if input_json['unset'] == False:
                    self.unset = True
                    self.to_lang = input_json['lang']
                    errors = False
            return errors
    def get_default_language(self) -> bool:
            if self.unset and self.to_lang:
                result = self.to_lang
            else:
                result = None
            return result

    def _check_lang(self, lang):
        if lang =="":
            return False
        if lang in self.translator.get_languages_list():
                return True
        return False
translator = RequestsHandler()
@get('/api/v1/available_languages')
def handler():
    try:
        result =  translator.get_languages_list()
        response.status = 200
        output_json = {'error' : False, 'languages' : result}
    except Exception as e:
        response.status = 500
        output_json = {'error' : True, 'description' : str(e)}
    return output_json
    
@post('/api/v1/translate')
def handler():
    try :
        result =  translator.translate(request.json)
        output_json = {"error" : False, "result" : result}
        return output_json

    except (TypeError, KeyError, ValueError) as e:
            output_json = {'error' : True,
                'description' : str(e)}
            response.status = 400
    except :
            output_json = {'error' : True,
                'description' : 'Unhandled exception'}
            response.status = 500
    return output_json

@post('/api/v1/default_language')
def handler():
    try:
        result = translator.save_default_language(request.json)
        output_json = {'error' : result}
        return output_json

    except (TypeError, KeyError, ValueError) as e:
        output_json = {'error' : True, 'description' : str(e)}
        response.status = 400
    except :
        output_json = {'error' : True, 'description' : 'Unhandled exception'}
        response.status = 500 
    return output_json

@get('/api/v1/default_language')
def handler():
    try:
        result = translator.get_default_language()
        output_json = {'error' : False, 'lang' : result}
    except :
        output_json = {'error' : True, 'description' : 'Unhandled exception'} 
        response.status = 500
    return output_json
run(host = localhost, port = port)