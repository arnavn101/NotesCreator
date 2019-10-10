import progress_bar
import os
import urllib.request

def download_required():
	print("\nDownloading ffmpeg dependencies\n")
	urllib.request.urlretrieve("https://blob-us-east-1-jrihav.s3.amazonaws.com/sara/7c/7c8b/7c8b86b6-560b-4018-9c49-bad448a304ab.bin?response-content-disposition=attachment%3B%20filename%3D%22ffmpeg.exe%22&response-content-type=application%2Foctet-stream&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAI75SICYCOZ7DPWTA%2F20191010%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20191010T230008Z&X-Amz-SignedHeaders=host&X-Amz-Expires=1800&X-Amz-Signature=7a12c57b5bebb6eabdf042b79cdea5dc3123c083e1c90a3faee1a42287b05c5d", "ffmpeg.exe", progress_bar.MyProgressBar()) # add windows/linux support

if not os.path.isfile("ffmpeg.exe") and os.name=="nt":
	download_required()