from typing import List
from threading import Thread

import time


class TaggedDocument:
    def __init__(self, id_, tag):
        self.id_ = id_
        self.tag = tag
        self.stored = False
    
    def to_json(self):
        return {
            "id": id_,
            "tag": tag
        }
    
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


    def persistance_thread(self):
        while 1:
            if self.stop_thread:
                self.stop_thread = False
                return
            undumped: List[TaggedDocument] = [document for document in self.documents if document.stored == False]
            for document in undumped:
                with open(self.storage_path + "/" + document.id_) as f:
                    json.dump(document.to_json(), f)
                    document.stored = True
            time.sleep(5)
    
    def start_persistance_thread(self):
        logging.error("Starting persistance thread")
        self.stop_thread = False
        self.persistance_thread = Thread(target=self.persistance_thread)
        self.persistance_thread.start()

    def stop_persistance_thread(self):
        if not self.persistance_thread:
            return False
        logging.error("Stopping persistance thread")
        self.stop_thread = True
        while 1:
            if not self.mtm_thread.is_alive():
                logging.error("Stopped persistance thread")
                return True