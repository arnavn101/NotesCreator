import os

def findNremove(path,pattern,maxdepth=1):
    cpath=path.count(os.sep)
    for r,d,f in os.walk(path):
        if r.count(os.sep) - cpath <maxdepth:
            for files in f:
                if files.endswith(pattern):
                    try:
                        print ("Removing %s" % (os.path.join(r,files)))
                        os.remove(os.path.join(r,files))
                    except Exception:
                        print (Exception)
                    else:
                        print ("%s removed" % (os.path.join(r,files)))

def execute():
	path=os.getcwd()
	to_remove = [".jpg", ".wav", ".jpeg", ".mp3", ".mp4", ".png"]
	
	for element in to_remove:
		findNremove(path, element)


