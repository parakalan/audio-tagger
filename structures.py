import os
from typing import List
from threading import Thread

import time
import json
import logging


class TaggedDocument:
    def __init__(self, id_, tag):
        self.id_ = id_
        self.tag = tag
        self.stored = False
    
    def to_json(self):
        return {
            "id": self.id_,
            "tag": self.tag
        }

    @staticmethod
    def from_json(payload):
        return TaggedDocument(id_=payload["id_"], tag=payload["tag"])


class TaggedDocumentPersistance:
    def __init__(self, storage_path):
        self.documents = []
        self.storage_path = storage_path
        self.stop_thread = False
        self.persistance_thread = None
    
    def add(self, tagged_document: TaggedDocument):
        self.documents.append(tagged_document)

    def persistance_fn(self):
        while 1:
            if self.stop_thread:
                self.stop_thread = False
                return
            undumped: List[TaggedDocument] = [document for document in self.documents if not document.stored]
            for document in undumped:
                with open(self.storage_path + "/" + document.id_.split("/")[-1] + ".json", "w") as f:
                    json.dump(document.to_json(), f)
                    document.stored = True
            time.sleep(5)
    
    def start_persistance_thread(self):
        os.makedirs(self.storage_path, exist_ok=True)
        logging.error("Starting persistance thread")
        self.stop_thread = False
        self.persistance_thread = Thread(target=self.persistance_fn)
        self.persistance_thread.start()

    def stop_persistance_thread(self):
        if not self.persistance_thread:
            return False
        logging.error("Stopping persistance thread")
        self.stop_thread = True
        while 1:
            if not self.persistance_thread.is_alive():
                logging.error("Stopped persistance thread")
                return True