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
    out = ''
    for key in res:
        out+= str(key +" " + res[key]) + "\n"
    return out


@post('/api/v1/translate')
def hundler():
    res = GoogleTranslator()
    for key in request.json:
        if key and request.json[key] and check_lang(request.json[key]) == False:
            return "Uncorrect language"
        if key and request.json[key] and check_lang(request.json[key]):
            return res.translate(text = key,to_lang=request.json[key])
            ### def lang is None
        if Unset and to_lang:
            ### def lang is True
            return res.translate(text = key,to_lang=to_lang)
        if key :
            return "Firtly imput default language"
        if key == None :
            return "Empty text"
        else:
            return "Empty text"
    return "Empty text"


@post('/api/v1/default_language')
def hundler():
    global Unset, to_lang
    for key in request.json:
        if check_lang(key) and Unset == False:
            ### change None -> def
            Unset = True
            to_lang = key
            return "Default language is " + str(to_lang)
        if check_lang(key) and Unset == True:
            ### change lang def -> def
            to_lang = key
            return "Default language is " + str(to_lang)
        if key == 'False' and Unset == True:
            ### change def -> None
            Unset == False
            to_lang = False
            return "Default language is not exhibited"
        else:
            return "Uncorrect language"
        

@get('/api/v1/get_default_language')
def hundler():
    if Unset and to_lang:
        return 'Default language is ' + str(to_lang)
    else:
        return 'Default language is not exhibited'

run(host='92.118.114.138', port=8080)