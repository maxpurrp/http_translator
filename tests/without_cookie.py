import requests

def get_lang_list():
    req = requests.get('http://92.118.114.138:8080/api/v1/available_languages')
    return req

def post_translate(output_json: dict):
    req = requests.post('http://92.118.114.138:8080/api/v1/translate',json=output_json)
    return req

def save_def_lang(output_json: dict):
    default_lang = requests.post('http://92.118.114.138:8080/api/v1/default_language',
                                 json=output_json)
    return default_lang

def get_def_lang():
    get_def = requests.get('http://92.118.114.138:8080/api/v1/default_language')
    return get_def

tests_for_trans = [{"text" : 'pool', "to_lang" :'ru'},
                {"text" : '', "to_lang" :''},
                {"text" : 'pool'}, 
                {}]
tests_for_post_lang = [{'unset' : False, 'lang' :  'ru'},
                       {'unset' : True,'lang' :  ''},
                       {'unset' : False, 'lang' :  'dd'},
                       {'unset' : False, 'lang' :  ''}]

class Tests_without_cookie():
    def __init__(self, *funcs, tests_for_trans, test_for_lang) -> None:
        self.funcs = funcs
        self.first_test = tests_for_trans
        self.second_test = test_for_lang

    def start_test(self):
        for elem in range(len(self.funcs)):
            print()
            if elem == 0:
                res = self.funcs[elem]()
                print(res.status_code)
            if elem == 1:
                print(f'Test for translate')
                for req in self.first_test:
                    res = res = self.funcs[elem](req)
                    print(f'output is {req}')
                    print(res.json())
                    print(res.status_code)
            if elem == 2:
                print(f'Test for post def lang')
                for req in self.second_test:
                    res = self.funcs[elem](req)
                    print(f'output is {req}')
                    print(res.json())
                    print(res.status_code)
            if elem == 3:
                print(f'Test for check def lang')
                res = self.funcs[elem]()
                print(res.status_code)
                print(f'Expected lang None')
                print(res.json())
res = Tests_without_cookie(get_lang_list,post_translate,save_def_lang,get_def_lang,tests_for_trans=tests_for_trans,test_for_lang=tests_for_post_lang)
res.start_test()
