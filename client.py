#!/usr/bin/python3
import requests

while True:
    x = int(input())
    if x == 1:
        r = requests.get('http://92.118.114.138:8080/api/v1/available_languages')
        print(r.text)
        continue
    if x == 2:
        text = input("word or sentenses ")
        to_lang = input('to_lang:')
        info = {text : to_lang}
        q = requests.post('http://92.118.114.138:8080/api/v1/translate',json=info)
        print(q.text)
        continue
    if x == 3:
        default_lang = requests.get('http://92.118.114.138:8080/api/v1/get_default_language')
        print(default_lang.text)
        continue
    if x == 4:
        info = {}
        lang = input('def lang is :')
        info[lang] = False
        default_lang = requests.post('http://92.118.114.138:8080/api/v1/default_language',json=info)
        print(default_lang.text)
        continue
    if x == 0 :
        break
