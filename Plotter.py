import os
import matplotlib.pyplot as plt
from pymongo import MongoClient, ASCENDING

connection_string = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/")
client = MongoClient(connection_string)
db = client['Restaurantdb']
collection = db['system_logs']

logs = list(collection.find().sort("timestamp", ASCENDING))

if not logs:
    print("Keine Daten vorhanden")
    exit()

zeiten = [log["timestamp"] for log in logs]
cpu_werte = [log["cpu"] for log in logs]
ram_prozent = [(log["ram_used"] / log["ram_total"]) * 100 for log in logs]

plt.figure(figsize=(10, 5))

plt.plot(zeiten, cpu_werte, label="CPU (%)", color="blue")
plt.plot(zeiten, ram_prozent, label="RAM (%)", color="green")

plt.xlabel("Zeit")
plt.ylabel("Auslastung in %")
plt.title("Systemauslastung")
plt.legend()
plt.grid(True)

plt.gcf().autofmt_xdate()
plt.show()