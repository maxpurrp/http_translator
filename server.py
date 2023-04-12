from bottle import get, post, request, response,  run # or route
from GoogleTranslator import GoogleTranslator
import sys

Unset = False
to_lang = False

def check_lang(lang):
    x = GoogleTranslator()
    x = x.get_languages_list()
    for key in x:
        if lang == x[key]:
            return True
    return False


@get('/api/v1/available_languages')
def hundler():
    try:
        res = GoogleTranslator()
        res = res.get_languages_list()
        out = []
        for key, value in res.items():
            out.append(value)
        ign = {"error": False, "languages" : out}
        return ign
    except :
        ign = {'error' : True,
            'description' : sys.exc_info()[1]}
        response.status = 500 
        return ign



@post('/api/v1/translate')
def hundler():
    try:
        res = GoogleTranslator()
        ign = request.json
        for key in ign:
            for elem in ign['text']:
                if elem.isdigit():
                    raise ValueError('Unsupported value format')
                
            if ign['text'] and check_lang(ign['to_lang']):
                result = res.translate(ign['text'],to_lang=ign['to_lang'])
                out = {"error" : False,
                    "result" : result}
                return out
            
            if ign['text'] and Unset == True:
                result = res.translate(ign['text'],to_lang=to_lang)
                out = {'error' : False,
                    'result' : result}
                return out
            
            if ign['text'] and ign['to_lang'] == '' and Unset == False:
                out = {'error' : True,
                    'description' : 'Firtly imput default language'}
                response.status = 400
                return out
            
            if ign['text'] and check_lang(ign['to_lang']) == False:
                out = {"error" : True,
                    "Description" : 'Unsupported language format'}
                response.status = 400
                return out
            
            if ign['text'] == "" :
                out = {'error' : True,
                    'description' : "Empty text"}
                response.status = 400
                return out
            
    except ValueError:
        ign = {'error' : True,
               'description' : 'Unsupported value format'}
        response.status = 400
        return ign
    
    except :
        ign = {'error' : True,
               'description' : str(sys.exc_info()[1])}
        response.status = 500
        return ign


@post('/api/v1/default_language')
def hundler():
    try:
        global Unset, to_lang
        ign = request.json
        for key in ign:
            for elem in ign['lang']:
                if elem.isdigit():
                    raise ValueError('Unsupported value format')
            
            if ign['lang'] == "":
                out = {'error' : True,
                    'description' : "Empty text"}
                response.status = 400
                return out
            
            if ign['Unset'] == False and check_lang(ign['lang']) == True:
                Unset = True
                to_lang = ign['lang']
                out = {'error' : False}
                return out
            
            if ign['Unset'] == False and check_lang(ign['lang']) == False:
                out = {'error' : True,
                    'description' : 'Unsupported language format'}
                response.status = 400
                return out
            
            if ign['Unset'] == True:
                Unset = False
                to_lang = False
                out = {'error' : False}
                return out
    
    except ValueError:
        ign = {'error' : True,
               'description' : 'Unsupported value format'}
        response.status = 400
        return ign

    except :
        ign = {'error' : True,
            'description' : str(sys.exc_info()[1])}
        response.status = 500 
        return ign
        


@get('/api/v1/default_language')
def hundler():
    try:
        if Unset and to_lang:
            out = {'error' : False,
                'lang' : to_lang}
            return out
        else:
            out = {'error' : False,
                'description' : 'Default language is not exhibited'}
            return out
    except  :
        ign = {'error' : True,
               'description' : sys.exc_info()[1]} 
        response.status = 500
        return ign
run(host='92.118.114.138', port=8080)