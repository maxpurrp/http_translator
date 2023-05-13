from bottle import get, post, request, response,  run # or route
from GoogleTranslator import GoogleTranslator
import random
import string

localhost, port = '92.118.114.138', 8080
clients_cookies = {}

def cookie_value() -> str:
    letters = string.ascii_lowercase
    result = ''.join(random.choice(letters) for i in range(random.randrange(20,35)))
    return result

def chech_cookie(cli_cookie : str) -> str:
    cookie = cli_cookie
    if cookie in clients_cookies.keys():
        return clients_cookies[cookie]
    else:
        return None

class RequestsHandler():
    def __init__(self, default_language = None) -> None:
        self.translator = GoogleTranslator()
        self.default_language = default_language

    def get_languages_list(self) -> list:
        return self.translator.get_languages_list()
    def translate(self, input) -> str:
        if input.json == None:
            raise TypeError('Expected json')
        if 'text' not in input.json or 'to_lang' not in input.json:
            raise KeyError('Expected text and to_lang in json')
        if self._check_lang(input.json['to_lang']) == False and self.default_language == None:
            raise ValueError('Invalid language')
        cur_lang = input.json['to_lang']
        if cur_lang == '':
            cookie = input.get_cookie(key='ssesion')
            if chech_cookie(cookie):
                cur_lang = chech_cookie(cookie)
            else:
                cur_lang = self.default_language
        result = self.translator.translate(input.json['text'],to_lang=cur_lang)
        return result
    def save_default_language(self, input_json) -> bool:
            if input_json == None:
                raise TypeError('Expected json')
            if 'unset' not in input_json:
                raise KeyError('Expected unset in json')
            
            if input_json['unset'] == True:
                    self.default_language = None
            else:
                if 'lang' not in input_json:
                    raise KeyError('Expected lang in json')
                if self._check_lang(input_json['lang']) == False:
                    raise ValueError('Invalid language')
                else:
                    self.default_language = input_json['lang']
            success = True
            return success
    def get_default_language(self, request):
            if chech_cookie(request.get_cookie(key='ssesion')) != None:
                return chech_cookie(request.get_cookie(key='ssesion'))
            else:
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
        result =  translator.translate(request)
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
        cli_cookie = request.get_cookie(key='ssesion')
        if cli_cookie in clients_cookies.keys():
            response.set_cookie(name='session', value=cli_cookie)
        else:
            #name = default name ; value = uniquely generated cookie
            response.set_cookie(name='session', value=cookie_value())
            sesi = str(response._cookies)
            clients_cookies[sesi.split('=')[1]] = request.json['lang']

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
        result = translator.get_default_language(request)
        output_json = {'error' : False, 'lang' : result}
    except Exception as e :
        output_json = {'error' : True, 'description' : 'Unhandled exception'} 
        response.status = 500
        print(e)
    return output_json
run(host = localhost, port = port)