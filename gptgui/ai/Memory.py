from datetime import datetime
import json
from hyperdb import HyperDB
from os import path

class Memory():
    def __init__(self, location:str) -> None:
        self._location = location
        self._json_loc = path.join(
            self._location, 
            "memories.jsonl")
        self._db_loc = path.join(
            self._location, 
            "db.pickle.gz")
        #CREATE _DOCUMENTS
        self._db = HyperDB(key="memory")
        if path.exists(self._db_loc):
            self._db.load(self._db_loc)
            print(self._db.documents)
        else:
            with open(self._db_loc, 'w'): pass


    def __len__(self):
        return len(self._db.documents)
    
    def save_memory(self, memory:str):
        memory_dic = {
            "memory": memory,
            "datetime": str(datetime.now())}
        self._db.add(memory_dic)
        self._db.save(self._db_loc)

    def load_memory(self, query:str):
        answer = self._db.query(query, top_k=3)
        print(answer)
        answer = [an for an in answer if an[1]>0.8]
        return answer
    
    