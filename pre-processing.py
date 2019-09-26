from pydub import AudioSegment
from pydub.utils import make_chunks
import os
import shutil
import ffmpeg
import glob
import magic

directory = "parts/"

def files(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file


if not os.path.isfile("audio.wav"):
    for filename in files(os.getcwd()):
        if "Audio" in magic.from_file(filename):
            input = ffmpeg.input(filename)
            output = ffmpeg.output(input, "audio.wav", format="wav")
            ffmpeg.run(output)


myaudio = AudioSegment.from_file("audio.wav" , "wav") 
chunk_length_ms = 30000 # pydub calculates in millisec

chunks = make_chunks(myaudio, chunk_length_ms) # Make chunks of 30 sec

if not os.path.exists(directory):
       os.makedirs(directory)
else:
    shutil.rmtree(directory)
    os.makedirs(directory)

for i, chunk in enumerate(chunks):
    chunk_name = "parts/{0}.wav".format(i)
    print ("Creating ", chunk_name)
    chunk.export(chunk_name, format="wav")
