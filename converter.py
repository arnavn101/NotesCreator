import subprocess

def convert(file_name):
        file = open(file_name, "r")
        text = file.readlines()

        with open("cmd.sh", "w+") as myfile:
                myfile.write('curl -d "text=' + text[0] + ' "' +  " http://bark.phon.ioc.ee/punctuator")
        
        finale = subprocess.check_output("sh cmd.sh", shell=True)
        output = str(finale, "utf-8")

        with open(file_name, 'w+') as file:
                file.write(output)

convert("text.txt")