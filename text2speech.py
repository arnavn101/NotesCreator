# importing modules
import os
import speech_recognition as sr
from multiprocessing.dummy import Pool
import re

class Text2Speech():
    
# Creating Recognizer object & assigning number for concurrent threads
    def __init__(self, threads, text_name):
        self.pool = Pool(int(threads)) 
        self.r = sr.Recognizer()
        self.files = []
        self.all_text = ""
        self.transcript = ""
        self.text_name = text_name
        self.create_list()
        self.init()
        self.join()
        self.write_file(self.text_name)
        
    # creating list for all parts of speech
    def create_list(self):
        self.files = os.listdir('parts/')
        self.files.sort(key=self.natural_keys)

    def atoi(self,text):
        return int(text) if text.isdigit() else text


    def natural_keys(self,text):
        '''
        alist.sort(key=natural_keys) sorts in human order
        http://nedbatchelder.com/blog/200712/human_sorting.html
        (Toothy's implementation in the comments)
        '''
        return [ self.atoi(c) for c in re.split(r'(\d+)', text) ]


    # converting audio to text
    def transcribe(self,data):
        idx,file = data
        name = "parts/" + file
        print(name + " started")
        
        # Load audio file
        with sr.AudioFile(name) as source:
            audio = self.r.record(source)
            
        # Transcribe audio file
        text = self.r.recognize_google(audio)
        print(name + " done")
        return {
            "text": text
        }
  
    # initializing threads and running them seperately
    def init(self):
        self.all_text = self.pool.map(self.transcribe, enumerate(self.files))
        self.pool.close()
        self.pool.join()
    
    # joinig individual elements of speech
    def join(self):
        for t in self.all_text:
            self.transcript = self.transcript + " " + t['text']
        print(self.transcript)
    
    # writing contents of speech to file
    def write_file(self,name):
        with open(str(self.text_name), "w+") as f:
            f.write(self.transcript)

a = Text2Speech(7, "text.txt")