import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


path_inhalt = os.environ.get("PATH")
if path_inhalt:
    print(path_inhalt)
else:
    print("Fehler: PATH nicht gefunden")

load_dotenv()

connection_string = os.environ.get("MONGODB_URI")
if not connection_string:
    print("Fehler: MONGODB_URI fehlt")
    exit()

try:
    client = MongoClient(connection_string, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    print("Verbindung erfolgreich")
except ConnectionFailure:
    print("Verbindung fehlgeschlagen")