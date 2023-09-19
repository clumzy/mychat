from datetime import datetime
import json
from hyperdb import HyperDB
from os import path

class MemoryService():
    def __init__(self, location:str) -> None:
        self._location = location
        self._json_loc = path.join(
            self._location, 
            "memories.jsonl")
        self._db_loc = path.join(
            self._location, 
            "db.pickle.gz")
        self._documents = self._generate_docs()

    def _generate_docs(self):
        with open (self._json_loc, "r") as f:
            self._documents = [json.loads(line) for line in f]
    
    def save_memory(self, memory:str):
        memory_dic = {
            "memory": memory,
            "datetime": str(datetime.now())}
        print(json.dumps(memory_dic))
        with open(self._json_loc, "a") as f:
            f.write(json.dumps(memory_dic)+"\n")
        f.close()
        self._generate_docs()
        db = HyperDB(self._documents, key="memory")
        db.save(self._db_loc)

    def load_memory(self, query:str):
        self._generate_docs()
        db = HyperDB(self._documents, key="memory")
        db.save(self._db_loc)        
        db.load(self._db_loc)
        answer = str(db.query(query, top_k=1)[0][0])
        print(answer)
        return str(db.query(query, top_k=1)[0][0])
    
    