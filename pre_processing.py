import install_dependencies
from pydub import AudioSegment
from pydub.utils import make_chunks
import os
import shutil
import ffmpeg
import glob
import magic
import sys
import urllib.request

class PreProcessor():
	def __init__(self):
		self.convert_audio()
		self.segment_audio()

	# get all files in dir
	def retrieve_files(self, path):
		for file in os.listdir(path):
		    if os.path.isfile(os.path.join(path, file)):
		        yield file

	# convert audio to wav format
	def convert_audio(self):
		if not os.path.isfile("audio.wav"):
		    for filename in self.retrieve_files(os.getcwd()):
		        if "Audio" in magic.from_file(filename) or "audio" in magic.from_file(filename):
		            input = ffmpeg.input(filename)
		            output = ffmpeg.output(input, "audio.wav", format="wav")
		            ffmpeg.run(output)

	# divide audio into several parts
	def segment_audio(self):
		myaudio = AudioSegment.from_file("audio.wav" , "wav") 
		chunk_length_ms = 30000 # pydub calculates in millisec
		directory = "parts/"

		chunks = make_chunks(myaudio, chunk_length_ms) # Make chunks of 30 sec
		self.create_dir(directory)

		for i, chunk in enumerate(chunks):
		    chunk_name = "parts/{0}.wav".format(i)
		    print ("Creating ", chunk_name)
		    chunk.export(chunk_name, format="wav")

	# create directory
	def create_dir(self, directory):
		if not os.path.exists(directory):
		       os.makedirs(directory)
		else:
		    shutil.rmtree(directory)
		    os.makedirs(directory)

