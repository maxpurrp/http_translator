from bottle import get, post, request, response,  run # or route
from GoogleTranslator import GoogleTranslator

localhost, port = '92.118.114.138', 8080
class RequestsHandler():
    def __init__(self, unset = False, default_language = None) -> None:
        self.translator = GoogleTranslator()
        self.default_language = default_language

    def get_languages_list(self) -> list:
        return self.translator.get_languages_list()
    def translate(self, input_json) -> str:
        if input_json == None:
            raise TypeError('Expected json')
        if 'text' not in input_json or 'to_lang' not in input_json:
            raise KeyError('Expected text and to_lang in json')
        if self._check_lang(input_json['to_lang']) == False and self.default_language == None:
            raise ValueError('Invalid language')
        cur_lang = input_json['to_lang']
        if cur_lang == '':
            cur_lang = self.default_language
        result = self.translator.translate(input_json['text'],to_lang=cur_lang)
        return result
    def save_default_language(self, input_json) -> bool:
            if input_json == None:
                raise TypeError('Expected json')
            if 'unset' not in input_json:
                raise KeyError('Expected unset in json')
            
            
            if input_json['unset'] == True:
                    self.unset = False
                    self.default_language = None
            else:
                if 'lang' not in input_json:
                    raise KeyError('Expected lang in json')
                if self._check_lang(input_json['lang']) == False:
                    raise ValueError('Invalid language')
                self.unset = True
                self.default_language = input_json['lang']
            success = True
            return success
    
    def get_default_language(self) -> bool:
            return self.default_language

    def _check_lang(self, lang):
        return lang in self.translator.get_languages_list()
translator = RequestsHandler()
@get('/api/v1/available_languages')
def handler():
    try:
        result =  translator.get_languages_list()
        response.status = 200
        output_json = {'error' : False, 'languages' : result}
    except Exception as e:
        response.status = 500
        output_json = {'error' : True, 'description' : 'Unhandled exception'}
        print(e)
    return output_json
    
@post('/api/v1/translate')
def handler():
    try :
        result =  translator.translate(request.json)
        output_json = {"error" : False, "result" : result}

    except (TypeError, KeyError, ValueError) as e:
            output_json = {'error' : True, 'description' : str(e)}
            response.status = 400
    except Exception as e  :
            output_json = {'error' : True, 'description' : 'Unhandled exception'}
            response.status = 500
            print(e)
    return output_json

@post('/api/v1/default_language')
def handler():
    try:
        if translator.save_default_language(request.json):
            output_json = {'error' : False}
        else:
             output_json = {'error' : True, 'description' : "Can't save default language"}

    except (TypeError, KeyError, ValueError) as e:
        output_json = {'error' : True, 'description' : str(e)}
        response.status = 400
    except Exception as e :
        output_json = {'error' : True, 'description' : 'Unhandled exception'}
        response.status = 500 
        print(e)
    return output_json

@get('/api/v1/default_language')
def handler():
    try:
        result = translator.get_default_language()
        output_json = {'error' : False, 'lang' : result}
    except Exception as e :
        output_json = {'error' : True, 'description' : 'Unhandled exception'} 
        response.status = 500
        print(e)
    return output_json
run(host = localhost, port = port)