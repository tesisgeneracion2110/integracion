import os
import time

from flask import Flask, request, abort, jsonify, send_from_directory, redirect, url_for
from __init__ import renderize_voice

UPLOAD_DIRECTORY = "."

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

api = Flask(__name__)
api.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


@api.route("/voice" , methods=[ 'POST'])
def voice():
    content = request.json
    print (content['out_name'])
    print (content['lyrics'])
    print (content['midi'])
    print (content['sex'])
    print (content['tempo'])
    print (content['method'])
    print (content['language'])
    renderize_voice(content['lyrics'], content['midi'],content['sex'] ,content['tempo'] ,'./archivos' , content['method'],content['language'$
    return jsonify({"download_link":"http://0.0.0.0:5000/files/"+"out_name"})

@api.route("/files" , methods = [ 'GET'])
def list_files():
    """Endpoint to list files on the server."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return jsonify(files)


@api.route("/files/<path:path>")
def get_file(path):
    """Download a file."""
    time.sleep(10)
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)
                                                                                                                                  
                                                                                                                                  
@api.route("/files/<filename>", methods=["POST"])
def post_file(filename):
    """Upload a file."""
    if "/" in filename:
        # Return 400 BAD REQUEST
        abort(400, "no subdirectories allowed")

    with open(os.path.join(UPLOAD_DIRECTORY, filename), "wb") as fp:
        fp.write(request.data)

    # Return 201 CREATED
    return "", 201
                                                                                                                                  
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

api.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
  # this has changed from the original example because the original did not work for me
    return filename[-3:].lower() in ALLOWED_EXTENSIONS

@api.route('/', methods=[ 'POST'])
def upload_file():
        file = request.files['file']
        print ('**found file', file.filename)
        #filename = secure_filename(file.filename)
        file.save(os.path.join(api.config['UPLOAD_FOLDER'], file.filename))
        # for browser, add 'redirect' function on top of 'url_for'
        return url_for('uploaded_file', filename=file.filename)

@api.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(api.config['UPLOAD_FOLDER'],filename)


if __name__ == "__main__":
    api.run(debug=True, host='0.0.0.0')
