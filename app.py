from flask import Flask, request
from flask import render_template

from structures import TaggedDocument, TaggedDocumentPersistance

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
    tagged_document_persistance.add(TaggedDocument.from_json(payload))
    return 200


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run", prefix_chars="-")
    parser.add_argument("-files_path", required=True, help="audio files path to tag", type=str)
    parser.add_argument("-extension", required=False, help="audio files extension", type=str)
    parser.add_argument("-storage_path", required=True, help="storage path for tagged documents", type=str)
    args = parser.parse_args()

    files = load_files(args.files_path, args.extension)
    tagged_document_persistance = TaggedDocumentPersistance(args.storage_path)
    tagged_document_persistance.start_persistance_thread()
    app.run(debug=False)