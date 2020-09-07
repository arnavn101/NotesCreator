# NotesCreator - v2.0

********
***Overview***
********

This repository provides a summarization tool which returns the
most "significant" sentences in a document, online article, or a video.
It uses a flask web framework and parses HTTP requests for 
parameters and attachments.

- ``NotesCreator``: HTTP Server that returns bullet point summaries
 

Functionality
=====

Fundamentally, ``NotesCreator`` is capable of 
    
    1) Parsing online articles and generating its summary 
  
    2) Converting audio to text in order to summarize it
    
    3) Taking Word Document, Pdf, or Image as Input and returning its summary
    
    4) Using IBM Watson to get tone of each sentence within a body of text
    
    5) Running a Web Server that handles POST requests for summaries and tone
    
    6) Handling GET requests for statistics on the host OS


************
Installation/Configuration
************

Linux Environments
==========================

On any Linux OS, clone this repository and setup API Keys
and Flask Credentials within the config file
 

      vim auth.cfg 
      

Install requirements of Python
    
    ./utils/install_all.sh
         

Run the Main File: 
     
     source flaskappenv/bin/activate 
     python3 flaskapp.py

Testing Summarizing Output with CURL
```bash 
curl -X POST  "http://127.0.0.1:5000/" \
              -d formIdentify=notes -d bullet_points=10 \
              -d URL=https://en.wikipedia.org/wiki/El_Dorado \
               -d choice=Website > index.html

firefox index.html # Can be any other browser
```


APIs and Resources Used
===============
      nltk
      SpeechRecognition
      FFmpeg-Python
      TextRact
      Readability-lxml
      # For more, refer to the requirements.txt file


