from flask import Flask
from flask import render_template

import os
import argparse

app = Flask(__name__)

files = []
tagged = []
current_idx = 0

def load_files(path, extension):
    files = os.listdir(path)
    files = [f for f in files if f.lower().endswith(extension.lower())]
    return files

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/tag", methods=["POST"])
def tag():
    payload = request.json["payload"]
    tagged.append({
        
    })


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run", prefix_chars="-")
    parser.add_argument("-files_path", required=True, help="specify audio files path", type=str)
    parser.add_argument("-extension", required=False, help="specify audio files extension", type=str)
    parser.add_argument("-persistance", required=False, help="specify end_date", type=str)
    args = parser.parse_args()

    files = load_files(args.files_path, args.extension)


    app.run(debug=True)