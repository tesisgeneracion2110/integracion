import wget
import os
import time
import requests
import constants as ct

from flask import Flask, request, abort, jsonify, send_from_directory, redirect, url_for

UPLOAD_DIRECTORY = "."

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

api = Flask(__name__)
api.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


def send_files_server(api_url, filename):
    fin = open(filename, 'rb')
    files = {'file': fin}
    try:
        r = requests.post(api_url, files=files)
        print(r.text)
    finally:
        fin.close()


def get_lyric_file(uri):
    print(uri)
    response = requests.get(uri)
    print("response: ", response)
    if response.status_code == 200:
        data = response.json()
        print("data lyric: ", data)
        lyric_download = ct.URI_LYRICS + ct.ENDPOINT_LYRIC_DOWNLOAD + "/" + data
        print("lyric_download: ", lyric_download)
        wget.download(lyric_download, ct.DIR_PATH_DOWNLOADS)
        return data
    return "error"


def generate_music(content):
    response = requests.post(ct.URI_MUSIC + ct.ENDPOINT_MUSIC, json=content)
    if response.status_code == 200:
        data = response.json()
        print("data music: ", data)
        midi = data['melody']
        # http://127.0.0.1:4000/music/file.mid
        midi_download = ct.URI_MUSIC + ct.ENDPOINT_MUSIC + "/" + midi
        wget.download(midi_download, ct.DIR_PATH_DOWNLOADS)
        print("midi_download: ", midi_download)

        wav = data['music']
        # http://127.0.0.1:4000/music/file.wav
        wav_download = ct.URI_MUSIC + ct.ENDPOINT_MUSIC + "/" + wav
        wget.download(wav_download, ct.DIR_PATH_DOWNLOADS)
        print("wav_download: ", wav_download)
        return {"midi": midi, "wav": wav, "bpm": data['bpm']}


@api.route("/song", methods=['POST'])
def generate_only_music():
    dir_files = generate_music(request.json)
    return jsonify(dir_files)


@api.route("/test")
def get_only_lyric():
    get_lyric_file(ct.URI_LYRICS + ct.ENDPOINT_LYRIC)
    return jsonify("terminated")


@api.route("/voice", methods=['POST'])
def voice():
    # Download and send lyric file
    dir_lyric = get_lyric_file(ct.URI_LYRICS + ct.ENDPOINT_LYRIC)
    send_files_server(ct.URI_VOICE_SEND, ct.DIR_PATH_DOWNLOADS + dir_lyric)
    print("entra 1")

    request_default = jsonify({
        "bpm": 90,
        "root": "A",
        "scale": "minor",
        "n_chords": 4,
        "progression": [3, 4, 5, 7],
        "n_beats": 2,
        "structure": [
            ["intro", 1],
            ["chorus", 1]
        ]
    })
    print("entra 2")
    #  Download and send midi, wav file
    dir_files = generate_music(request_default)
    send_files_server(ct.URI_VOICE_SEND, ct.DIR_PATH_DOWNLOADS + dir_files['midi'])
    #send_files_server(ct.URI_WAV, ct.DIR_PATH_DOWNLOADS + dir_files['wav'])

    # bpm, how to send?

    request_default_voice = jsonify(
        {
            "out_name": ct.VOICE_OUT_NAME,
            "lyrics": dir_lyric,
            "midi": dir_files['midi'],
            "sex": "male",
            "tempo": dir_files['bpm'],
            "method": 1,
            "language": "es"
        }
    )
    response = requests.post(ct.URI_VOICE, json=request_default_voice)
    wget.download(ct.URI_FILES + ct.VOICE_OUT_NAME, ct.DIR_PATH_DOWNLOADS)
    wget.download(ct.URI_VOICE_XML)

    return jsonify(
        {
            "lyric": dir_lyric,
            "voice": ct.VOICE_OUT_NAME,
            "melody": dir_files['midi'],
            "music": dir_files['wav']
        }
    )


@api.route("/files", methods=['GET'])
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


UPLOAD_FOLDER = '.'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

api.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# def allowed_file(filename):
# this has changed from the original example because the original did not work for me
# return filename[-3:].lower() in ALLOWED_EXTENSIONS


@api.route('/', methods=['POST'])
def upload_file():
    file = request.files['file']
    print('**found file', file.filename)
    # filename = secure_filename(file.filename)
    file.save(os.path.join(api.config['UPLOAD_FOLDER'], file.filename))
    # for browser, add 'redirect' function on top of 'url_for'
    return url_for('uploaded_file', filename=file.filename)


@api.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(api.config['UPLOAD_FOLDER'], filename)


if __name__ == "__main__":
    api.run(debug=True, port=8000)
