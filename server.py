from bottle import get, post, request, response,  run # or route
from GoogleTranslator import GoogleTranslator

class Sub_Class_Google(GoogleTranslator):
    def __init__(self, Unset = False, to_lang = None) -> None:
        self.method = GoogleTranslator()
        self.Unset = Unset
        self.to_lang = to_lang

clas_methods = Sub_Class_Google()
def check_lang(lang):
    if lang == "":
        return False
    else:
        for value in clas_methods.get_languages_list().values():
            if lang == value:
                return True
        return False
def check_word_or_sentence(text):
    if text == "":
        return True
    else:
        update = text.split()
        for elem in update:
            for i in range(len(elem)-1):
                if elem[i].isalpha() and elem[i+1].isnumeric() or elem[i+1].isalpha() and elem[i].isnumeric():
                    return True
        return False

@get('/api/v1/available_languages')
def handler():
    try:
        out_list = []
        for value in clas_methods.get_languages_list().values():
            out_list.append(value)
        output_json = {"error": False, "languages" : out_list}
        return output_json
    except :
        output_json = {'error' : True,
            'description' : 'Unhandled exception'}
        response.status = 500 
        return output_json


@post('/api/v1/translate')
def handler():
    try:
        input_json = request.json
        if input_json == {}:
            raise KeyError("Excpected json as input")
        if check_word_or_sentence(input_json['text']):
            raise ValueError('Unsupported value format')
        if check_lang(input_json['to_lang']) == False and clas_methods.to_lang == None:
            raise ValueError('Unsupported value format')
        for _ in input_json:  
            if input_json['text'] and check_lang(input_json['to_lang']):
                result = clas_methods.translate(input_json['text'],to_lang=input_json['to_lang'])
                output_json = {"error" : False,
                    "result" : result}
                return output_json
            if input_json['text'] and clas_methods.to_lang != None:
                result = clas_methods.translate(input_json['text'],to_lang=clas_methods.to_lang)
                output_json = {'error' : False,
                    'result' : result}
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


@post('/api/v1/default_language')
def handler():
    try:
        input_json = request.json
        if input_json == {}:
            raise KeyError("Excpected json as input")
        
        if input_json['Unset'] == True:
                    clas_methods.Unset = False
                    clas_methods.to_lang = None
                    output_json = {'error' : False}
                    return output_json

        if check_lang(input_json['lang']) == True:
            for _ in input_json:
                if input_json['Unset'] == False:
                    clas_methods.Unset = True
                    clas_methods.to_lang = input_json['lang']
                    output_json = {'error' : False}
                    return output_json
            
                if input_json['Unset'] == False:
                    output_json = {'error' : True,
                        'description' : 'Unsupported language format'}
                    response.status = 400
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
        

@get('/api/v1/default_language')
def handler():
    try:
        if clas_methods.Unset and clas_methods.to_lang:
            output_json = {'error' : False,
                'lang' : clas_methods.to_lang}
            return output_json
        else:
            output_json = {'error' : False,
                'lang' : None}
            return output_json
    except  :
        output_json = {'error' : True,
               'description' : 'Unhandled exception'} 
        response.status = 500
        return output_json
    

run(host='92.118.114.138', port=8080)