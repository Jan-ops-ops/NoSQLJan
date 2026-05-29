import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.dates as mdates
from pymongo import MongoClient, ASCENDING

connection_string = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/")
client = MongoClient(connection_string)
db = client['Restaurantdb']
collection = db['system_logs']

fig, ax = plt.subplots(figsize=(10, 5))

def update(frame):
    logs = list(collection.find().sort("timestamp", ASCENDING))[-30:]
    
    if not logs:
        return
        
    zeiten = [log["timestamp"] for log in logs]
    cpu_werte = [log["cpu"] for log in logs]
    ram_prozent = [(log["ram_used"] / log["ram_total"]) * 100 for log in logs]
    
    ax.clear()
    ax.plot(zeiten, cpu_werte, label="CPU (%)", color="blue")
    ax.plot(zeiten, ram_prozent, label="RAM (%)", color="green")
    
    ax.xaxis.set_major_locator(mdates.SecondLocator(interval=5))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    
    ax.set_xlabel("Zeit")
    ax.set_ylabel("Auslastung in %")
    ax.set_title("Systemauslastung")
    ax.legend()
    ax.grid(True)
    
    fig.autofmt_xdate()

ani = animation.FuncAnimation(fig, update, interval=1000, cache_frame_data=False)
plt.show()