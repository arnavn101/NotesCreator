from flask import Flask, render_template, request
from fetch import *
import image2text
import pre_processing
from punctuate import *
import summarizer
import text2speech
from shutil import copyfile
import urllib
import os
import progress_bar

app = Flask(__name__)

def extract_extension(string):
	return string[string.rindex('.')+1:] #add windows/linux support later

@app.route('/')
def data():
   return render_template('test.html')

@app.route('/result', methods = ['POST', 'GET'])
def result():
	if request.method == 'POST':
		bullet_points = request.form.get("bullet-points")
		url = request.form.get("URL")
		choice = request.form.get("choice")
		cd = os.getcwd()

		if choice == "Website":
			scrape_web("text.txt", url)
		elif choice == "Image":
			print("\nDownloading image\n")
			urllib.request.urlretrieve(url, "audio." + extract_extension(url), progress_bar.MyProgressBar())
			image2text.Image2Text("text.txt", "image_name")
		elif choice == "Video":
			print("\nDownloading video\n")
			urllib.request.urlretrieve(url, "image." + extract_extension(url), progress_bar.MyProgressBar())
			pre_processing.PreProcessor()
			text2speech.Text2Speech(bullet_points, "text.txt")
			convert_text("text.txt")

		
		a = summarizer.Summarizer("text.txt", int(bullet_points))
		txt = a.return_summary()
		return render_template('results.html', value=txt)
      
      
if __name__ == '__main__':
   app.run(host='127.0.0.1',port=12345)
