import os
import time
from datetime import datetime
import psutil
from pymongo import MongoClient, ASCENDING

connection_string = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/")
client = MongoClient(connection_string)
db = client['Restaurantdb']
collection = db['system_logs']

class Power:
    def __init__(self, cpu=None, ram_total=None, ram_used=None, timestamp=None):
        if cpu is None and ram_total is None and ram_used is None and timestamp is None:
            self.cpu = psutil.cpu_percent(interval=None)
            ram = psutil.virtual_memory()
            self.ram_total = ram.total
            self.ram_used = ram.used
            self.timestamp = datetime.now()
        else:
            self.cpu = cpu
            self.ram_total = ram_total
            self.ram_used = ram_used
            self.timestamp = timestamp

    def to_dict(self):
        return {
            "cpu": self.cpu,
            "ram_total": self.ram_total,
            "ram_used": self.ram_used,
            "timestamp": self.timestamp
        }

psutil.cpu_percent(interval=None)
time.sleep(0.1)

print("Logger gestartet...")
while True:
    log_daten = Power()
    collection.insert_one(log_daten.to_dict())
    
    anzahl = collection.count_documents({})
    if anzahl > 10000:
        ueberschuss = anzahl - 10000
        aelteste = collection.find({}, {"_id": 1}).sort("timestamp", ASCENDING).limit(ueberschuss)
        ids_zum_loeschen = [doc["_id"] for doc in aelteste]
        collection.delete_many({"_id": {"$in": ids_zum_loeschen}})
        
    time.sleep(1)