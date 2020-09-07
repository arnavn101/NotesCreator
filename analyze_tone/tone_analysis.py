import requests
import json
import os
import fileinput
import sys
import configparser
sys.path.insert(0, os.getcwd())  # Resolve Importing errors


class Tone_Analysis:
    def __init__(self, text_required):
        self.headers = {
            'Content-Type': 'application/json',
        }

        self.params = (
            ('version', '2017-09-21'),
        )

        self.file_path = os.path.join("analyze_tone", "tone.json")
        self.initial_config()
        text_required = (text_required.replace('"', '')).replace("'", '')
        self.configure_json('"' + text_required.strip() + '"', "{text}")
        self.data = open(self.file_path, 'rb').read()
        self.tone_text = " "
        self.sentence_tone = ""
        self.tone_sentences = ""

        self.config = configparser.ConfigParser()
        self.config.read('config.cfg')
        self.WATSON_API_KEY = str(self.config.get('ConfigInfo', 'WATSON_API_KEY'))

        self.json_object = json.loads((self.analyze_tone_watson()).text)
        self.retrieve_sentiments()
        self.finale()
        self.configure_json("{text}", '"' + text_required + '"')

    def configure_json(self, replacement_text, text_toBe_replaced):
        with fileinput.FileInput(self.file_path, inplace=True) as file:
            for line in file:
                print(line.replace(text_toBe_replaced, replacement_text), end='')

    def initial_config(self):
        f = open(self.file_path, "w+")
        f = open(self.file_path, "w+")
        f.write('{\n"text": {text}\n}')
        f.close()

    def analyze_tone_watson(self):
        response = requests.post('https://gateway.watsonplatform.net/tone-analyzer/api/v3/tone', headers=self.headers,
                                 params=self.params, data=self.data,
                                 auth=('apikey', self.WATSON_API_KEY))
        return response

    def retrieve_sentiments(self):
        for x in range(0, len(self.json_object["document_tone"]["tones"])):
            self.tone_text += (self.json_object["document_tone"]["tones"][x]["tone_name"] + ", ")

        try:
            for x in range(0, len(self.json_object["sentences_tone"])):
                for y in range(0, len(self.json_object["sentences_tone"][x]["tones"])):
                    self.sentence_tone += (self.json_object["sentences_tone"][x]["tones"][y]["tone_name"] + ", ")

                if self.sentence_tone[:-2]:
                    self.tone_sentences += "Sentence " + str(x + 1) + ": " + self.sentence_tone[:-2] + "\n"
                self.sentence_tone = ""
        except Exception:
            self.tone_sentences = ""
            self.sentence_tone = ""

    def finale(self):
        if not self.tone_sentences:
            return "\n\nTone of entire text:" + self.tone_text[:-2]
        else:
            return "\n\nTone of entire text:" + self.tone_text[:-2] + "\n\n" + self.tone_sentences
