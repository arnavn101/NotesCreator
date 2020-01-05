import progress_bar
import os
import urllib.request
import zipfile
import sys
from shutil import copyfile

cd = os.getcwd()

def download_required(file_name, url):
	print("\nDownloading " + file_name + "\n")
	urllib.request.urlretrieve(url, file_name, progress_bar.MyProgressBar()) # add windows/linux support

if not os.path.isfile("ffmpeg.exe") and os.name=="nt":
	download_required("ffmpeg.zip","https://www.videohelp.com/download/ffmpeg-4.2.1-win32-static.zip?r=bFphdJvGrFQ")

	with zipfile.ZipFile("ffmpeg.zip", 'r') as zip_ref:
		zip_ref.extractall(cd)

	copyfile("ffmpeg-4.2.1-win32-static\\bin\\ffmpeg.exe", "ffmpeg.exe")

if not os.path.isfile("C:\\Program Files\\Tesseract-OCR\\tesseract.exe") and os.name=="nt":
	download_required("tesseract-ocr-w64-setup-v5.0.0-alpha.20191010.exe", "https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.0.0-alpha.20191010.exe")
	os.startfile("tesseract-ocr-w64-setup-v5.0.0-alpha.20191010.exe")

