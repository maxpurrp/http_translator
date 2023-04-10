from bottle import get, post, request, run # or route
from GoogleTranslator import GoogleTranslator


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
    res = GoogleTranslator()
    res = res.get_languages_list()
    out = []
    for key, value in res.items():
        out.append(value)
    ign = {"error": False, "languages" : out}
    return ign
    

@post('/api/v1/translate')
def hundler():
    res = GoogleTranslator()
    ign = request.json
    for key in ign:
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
            return out
        if ign['text'] and check_lang(ign['to_lang']) == False:
            out = {"error" : True,
                "Description" : 'Unsupported language format'}
            return out
        if ign['text'] == "" :
            out = {'error' : True,
                   'description' : "Empty text"}
            return out


@post('/api/v1/default_language')
def hundler():
    global Unset, to_lang
    ign = request.json
    for key in ign:
        if ign['Unset'] == False and check_lang(ign['lang']) == True:
            Unset = True
            to_lang = ign['lang']
            out = {'error' : False}
            return out
        if ign['Unset'] == False and check_lang(ign['lang']) == False:
            out = {'error' : True,
                   'description' : 'Unsupported language format'}
            return out
        if ign['Unset'] == True:
            Unset = False
            to_lang = False
            out = {'error' : False}
            return out


@get('/api/v1/get_default_language')
def hundler():
    if Unset and to_lang:
        out = {'error' : False,
               'lang' : to_lang}
        return out
    else:
        out = {'error' : True,
               'description' : 'Default language is not exhibited'}
        return out

run(host='92.118.114.138', port=8080)