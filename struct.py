from typing import List


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


class TaggedDocumentPersistance:
    def __init__(self, storage_path):
        self.documents = []
        self.storage_path = storage_path
    
    def add(self, tagged_document: TaggedDocument):
        self.documents.append(tagged_document)


    def persistance_thread(self):
        undumped: List[TaggedDocument] = [document for document in self.documents if document.dumped = stored]
        for document in undumped:
            with open(self.storage_path + "/" + document.id_) as f:
                json.dump(document.to_json(), f)
