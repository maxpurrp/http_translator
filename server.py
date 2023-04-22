from bottle import get, post, request, response,  run # or route
from GoogleTranslator import GoogleTranslator

localhost, port = '92.118.114.138', 8080
class RequestsHandler():
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
            if input_json == None:
                raise TypeError('Expected json')
            if input_json == {}:
                raise KeyError("Excpected json as input")
            if 'text' not in input_json or 'to_lang' not in input_json:
                raise ValueError('Unsupported value format')
            if self._check_lang(input_json['to_lang']) == False and self.to_lang == None:
                raise ValueError('Unsupported value format')
            cur_lang = input_json['to_lang']
            if cur_lang == '':
                cur_lang = self.to_lang
            output_json = {"error" : False, "result" : str(self.translator.translate(input_json['text'],to_lang=cur_lang))}
            return output_json
        
        except TypeError as e:
            output_json = {'error' : True,
                'description' : str(e)}
            response.status = 400
            return output_json
        
        except KeyError as e:
            output_json = {'error' : True,
                'description' : str(e)}
            response.status = 400
            return output_json
        
        except ValueError as e:
            output_json = {'error' : True,
                'description' : str(e)}
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
            if input_json == None:
                raise TypeError('Expected json')
            if 'to_lang' not in input_json or 'Unset' not in input_json:
                raise ValueError('Unsupported value format')
            
            if input_json['Unset'] == True:
                    self.Unset = False
                    self.to_lang = None
                    output_json = {'error' : False}

            if self._check_lang(input_json['lang']) == True:
                for _ in input_json:
                    if input_json['Unset'] == False:
                        self.Unset = True
                        self.to_lang = input_json['lang']
                        output_json = {'error' : False}      
            else:
                output_json = {'error' : True,
                'description' : 'Unsupported language format'}
                response.status = 400
            return output_json
        
        except ValueError as e:
            output_json = {'error' : True,
               'description' : str(e)}
            response.status = 400
            return output_json
        
        except TypeError as e:
            output_json = {'error' : True,
               'description' : str(e)}
            response.status = 400
            return output_json
        
        except KeyError as e:
            output_json = {'error' : True,
               'description' : str(e)}
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
run(host = localhost, port = port)
