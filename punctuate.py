import subprocess
import os
import requests

def convert(file_name):
        file = open(file_name, "r")
        text = file.readlines()
        url = 'http://bark.phon.ioc.ee/punctuator'

        data = {
        'text': text
        }

        response = requests.post(url, data=data)
        response_final = response.text

        with open(file_name, 'w+') as file:
                file.write(response_final)

convert("text.txt")