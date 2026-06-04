import os
from dotenv import load_dotenv
from pymongo import MongoClient

from Daoroom import Dao_room
from jokes import Joke, Dao_joke
from room import Room

def main():
    load_dotenv()
    connection_string = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/")

 
    print("[Test")
    joke_dao = Dao_joke(connection_string)
    
    neuer_witz = Joke(
        text="Warum fliegen Vögel im Winter in den Süden? Weil Laufen zu lange dauert.",
        category=["Flachwitz", "Tiere"],
        author="Jan"
    )
    
    joke_id = joke_dao.insert(neuer_witz)
    print(f"[Joke-Test] Witz eingefügt. ID: {joke_id}")
    
    gefundene_witze = joke_dao.get_category("Flachwitz")
    for witz in gefundene_witze:
        print(f" -> Gefunden: '{witz.text}' (von {witz.author})")
        
    joke_geloescht = joke_dao.delete(joke_id)
    print(f"[Joke-Test] Löschen erfolgreich: {joke_geloescht}\n")



if __name__ == "__main__":
    main()