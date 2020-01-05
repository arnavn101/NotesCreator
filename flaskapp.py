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
import paraphraser
import tone_analysis
from delete_useless import *
import textract
from werkzeug.utils import secure_filename


app = Flask(__name__)

def extract_extension(string):
	return string[string.rindex('.')+1:] 

@app.route('/', methods = ['POST', 'GET'])
def result():
	if request.method == 'POST':
		try:
				
			identifier = request.form.get("formIdentify")
			execute()		
			if identifier == "notes":
				bullet_points = request.form.get("bullet_points")
				url = request.form.get("URL")
				choice = request.form.get("choice")
				cd = os.getcwd()

				if choice == "Website":
					scrape_web("text.txt", url)

				elif choice == "Image":
					print("\nDownloading image\n")
					urllib.request.urlretrieve(url, "image." + extract_extension(url), progress_bar.MyProgressBar())
					image2text.Image2Text("text.txt", "image." + extract_extension(url))

				elif choice == "Attachment":
					print("Retrieving attached file")
					file_uploaded = request.files['myfile']
					filename = secure_filename(file_uploaded.filename)
					filepath = os.path.join(cd, filename)
					file_uploaded.save(filepath)
					list_valid_extensions = ["txt", "doc", "pdf", "csv","jpg", "msg", "png", "docx"]
					if extract_extension(filename) in list_valid_extensions: 
						text = textract.process(filepath)
						with open("text.txt", "wb+") as myfile:
							myfile.write(text)		
					else:
						pre_processing.PreProcessor()
						text2speech.Text2Speech(bullet_points, "text.txt")
						convert_text("text.txt")
						
				elif choice == "Audio":
					print("\nDownloading video\n")
					urllib.request.urlretrieve(url, "video." + extract_extension(url), progress_bar.MyProgressBar())
					pre_processing.PreProcessor()
					text2speech.Text2Speech(bullet_points, "text.txt")
					convert_text("text.txt")
							
				a = summarizer.Summarizer("text.txt", int(bullet_points))
				txt = (a.return_summary()).splitlines()
				return render_template('results.html', value=txt)
			
			elif identifier == "paraphrase":
				text_required = request.form.get("text_paraphrase")
				paraphraser_program = paraphraser.Paraphrase_Text(text_required)
				paraphraser_text = [(paraphraser_program.return_paraphrased())]
				return render_template('results.html', value=paraphraser_text)
			
			elif identifier == "tone_analyze":
				text_required = request.form.get("text_toning")
				toneAnalyzer_program = tone_analysis.Tone_Analysis(text_required)
				resultant_text = ((toneAnalyzer_program.finale()).splitlines())
				return render_template('results.html', value=resultant_text)
		except Exception as e:
			print(e)
			return render_template('results.html', value=["There was an error in running the application. Please verify that all information is properly entered."])

	  
	return ""
      
if __name__ == '__main__':
   app.run(host='0.0.0.0')
