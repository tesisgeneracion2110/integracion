import os
import time

from flask import Flask, request, abort, jsonify, send_from_directory, redirect, url_for


UPLOAD_DIRECTORY = "."

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

api = Flask(__name__)

@api.route("/prueba" , methods=[ 'POST'])
def prueba():
    content=request.json
    print(content['hola'])
    """Endpoint to list files on the server."""

    return "hola"

if __name__ == "__main__":
    api.run(debug=True, port=8000)
