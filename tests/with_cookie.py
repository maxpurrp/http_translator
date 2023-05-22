import requests

def get_lang_list():
    req = requests.get('http://92.118.114.138:8080/api/v1/available_languages')
    return req

def post_translate(output_json: dict, cookie : dict):
    req = requests.post('http://92.118.114.138:8080/api/v1/translate',json=output_json, cookies=cookie)
    return req

def save_def_lang(output_json: dict, cookie : dict):
    default_lang = requests.post('http://92.118.114.138:8080/api/v1/default_language',
                                 json=output_json, cookies=cookie)
    return default_lang

def get_def_lang(cookie):
    get_def = requests.get('http://92.118.114.138:8080/api/v1/default_language', cookies=cookie)
    return get_def

first_cookie = None
second_cookie = None
print(f'send request on post def lang ru')
default_lang_ru = save_def_lang({'unset' : False, 'lang' :  'ru'}, cookie = None)
print(default_lang_ru.status_code)
print(default_lang_ru.json())
print(default_lang_ru.headers['Set-Cookie'])
print(f'cookie first user, who take def lang is ru')
first_cookie = default_lang_ru.headers['Set-Cookie'].split('=')[1]
print()
print(f'send request on post def lang fr ')
default_lang_fr = save_def_lang({'unset' : False, 'lang' :  'fr'}, cookie = None)
print(default_lang_fr.status_code)
print(default_lang_fr.json())
print(default_lang_fr.headers['Set-Cookie'])
print(f'cookie second user, who take def lang is fr')
second_cookie = default_lang_fr.headers['Set-Cookie'].split('=')[1]
print()
print(f'request to receive default lang with cookie')
get_def = get_def_lang({'ssesion' :first_cookie})
print(f'Expected lang : ru')
print(get_def.json())
print()
print(f'request to receive default lang with cookie')
get_def = get_def_lang({'ssesion' :second_cookie})
print(f'Expected lang : fr')
print(get_def.json())
print()
print(f'request to receive default lang without cookie')
get_def = get_def_lang(None)
print(f'Expected lang : None')
print(get_def.json())
print(f'but response is def land - fr')
print()
print(f'request for translate on default lang with cookie (ru)')
trans = post_translate({"text" : 'pool', "to_lang" :''}, cookie={'ssesion' :first_cookie})
print(trans.json())
print()

print(f'request for translate on default lang with cookie (fr)')
trans_1 = post_translate({"text" : 'pool', "to_lang" :''}, cookie={'ssesion' :second_cookie})
print(trans_1.json())


