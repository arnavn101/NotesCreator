import subprocess
import os
import requests

# Punctuating text with outside resource
def convert_text(file_name):
        file = open(file_name, "r")
        text = file.read().replace('\n', '')
        url = 'http://bark.phon.ioc.ee/punctuator'

        data = {
        'text': text
        }

        # Sending request to punctuator via curl-like command
        response = requests.post(url, data=data)
        response_final = response.text

        write_file(file_name, response_final)

# Writing contents of response to file
def write_file(file_name, content):
	with open(file_name, 'w+') as file:
                file.write(content)

