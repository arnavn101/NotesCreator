import os
import pprint
import psutil
import requests
import configparser
from utils import manageFunction
from werkzeug.utils import secure_filename
from flask_httpauth import HTTPBasicAuth
from flask_restful import Resource, Api
from flask import Flask, render_template, request, jsonify, Response

"""
Basic Flask Configuration
"""

flask_application = Flask(__name__)
api = Api(flask_application, prefix="/api/v1/cmd")
pp = pprint.PrettyPrinter(indent=4)

auth = HTTPBasicAuth()
config = configparser.ConfigParser()
config.read('config.cfg')

USERNAME = str(config.get('ConfigInfo', 'USERNAME'))
PASSWORD = str(config.get('ConfigInfo', 'PASSWORD'))

USER_DATA = {
    USERNAME: PASSWORD
}


def extract_extension(string):
    return string[string.rindex('.') + 1:]


def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f} {unit}{suffix}"
        bytes /= factor


@auth.verify_password
def verify(username, password):
    if not (username and password):
        return False
    return USER_DATA.get(username) == password


class retrieve_information(Resource):
    @auth.login_required
    def get(self):
        return jsonify(
            Total_CPU_Usage=f"{psutil.cpu_percent()}%",
            Total_Memory_Usage=f"{psutil.virtual_memory().percent}%",
            Free_Disk_Space=f"{get_size(psutil.disk_usage('/').free)}",
            Network_Bandwidth=f"{get_size(psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv)}")


@flask_application.route('/', methods=['POST', 'GET'])
def handle_inputData():
    if request.method == 'POST':
        try:
            # Handle POST Request Accordingly
            function_identifier = request.form.get("formIdentify")
            list_arguments = {"function_identifier": function_identifier}

            if function_identifier == "notes":
                list_arguments["bullet_points"] = request.form.get("bullet_points")
                list_arguments["specified_url"] = request.form.get("URL")
                list_arguments["operation_choice"] = request.form.get("choice")

                if list_arguments["operation_choice"] == "Attachment":
                    print("Retrieving attached file")
                    file_uploaded = request.files['myfile']
                    filename = secure_filename(file_uploaded.filename)
                    filepath = os.path.join("downloads", filename)
                    file_uploaded.save(filepath)

                    list_valid_extensions = ["txt", "doc", "pdf", "csv", "jpg", "msg", "png", "docx"]
                    if extract_extension(filename) in list_valid_extensions:
                        list_arguments["minor_operation"] = "valid_extensions"
                        list_arguments["file_path"] = filepath
                    else:
                        list_arguments["minor_operation"] = "invalid_extensions"

                task_execution = manageFunction.ManageTask(**list_arguments)
                return render_template('results.html', value=task_execution.return_text())

            elif function_identifier == "tone_analyze":
                list_arguments["text_required"] = request.form.get("text_toning")
                task_execution = manageFunction.ManageTask(**list_arguments)
                return Response(response=render_template('results.html', value=task_execution.return_text()))

        except requests.exceptions.ReadTimeout:
            return render_template('results.html', value=["Sorry."
                                                          " The inputted Website is not supported for summaries."])
        except Exception as error_app:
            pp.pprint(error_app)
            return render_template('results.html', value=["There was an error in running the application."
                                                          " Please verify that all information is properly entered."])

    # Prevent error in Case of weird types of requests
    return ""


# Add resource to the api
api.add_resource(retrieve_information, '/stats')

if __name__ == '__main__':
    flask_application.run(host='0.0.0.0')
