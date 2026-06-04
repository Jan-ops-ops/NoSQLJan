import os
import sys
from pymongo import MongoClient
import gridfs
from bson.objectid import ObjectId

# Datenbank-Setup
client = MongoClient("mongodb://localhost:27017/")
db = client["jukebox_db"]
songs_collection = db["songs"]
bucket = gridfs.GridFSBucket(db, bucket_name="audio_tracks")

class Song:
    """Klasse repräsentiert ein Musikstück mit seinen Attributen."""
    def __init__(self, title, artist, album=None, genre=None, year=None, file_id=None):
        self.title = title
        self.artist = artist
        self.album = album
        self.genre = genre
        self.year = year
        self.file_id = file_id 

    def to_dict(self):
        """Konvertiert das Objekt in ein MongoDB-taugliches Dictionary."""
        return {
            "title": self.title,
            "artist": self.artist,
            "album": self.album,
            "genre": self.genre,
            "year": self.year,
            "file_id": self.file_id
        }

def song_hinzufuegen():
    print("\n--- SONG HINZUFÜGEN ---")
    title = input("Titel (Pflichtfeld): ").strip()
    artist = input("Interpret (Pflichtfeld): ").strip()
    if not title or not artist:
        print("Fehler: Titel und Interpret dürfen nicht leer sein!")
        return

    album = input("Album (Optional): ").strip() or None
    genre = input("Genre (Optional): ").strip() or None
    year_input = input("Erscheinungsjahr (Optional): ").strip()
    year = int(year_input) if year_input.isdigit() else None
    
    audio_pfad = input("Pfad zur Audio-Datei (z.B. song.mp3): ").strip()
    
    file_id = None
    if audio_pfad and os.path.exists(audio_pfad):
        with open(audio_pfad, "rb") as f:
            file_id = bucket.upload_from_stream(os.path.basename(audio_pfad), f)
        print("Audio-Datei erfolgreich in GridFS gespeichert.")
    else:
        print("Hinweis: Keine oder ungültige Audio-Datei angegeben. Song wird ohne Audio angelegt.")

    neuer_song = Song(title, artist, album, genre, year, file_id)
    songs_collection.insert_one(neuer_song.to_dict())
    print(f"Song '{title}' von '{artist}' erfolgreich erfasst!")

def song_suchen_und_waehlen():
    """Hilfsfunktion, um Songs für Edit/Delete zu finden."""
    suchbegriff = input("Nach welchem Song/Interpret suchen?: ").strip()
    query = {
        "$or": [
            {"title": {"$regex": suchbegriff, "$options": "i"}},
            {"artist": {"$regex": suchbegriff, "$options": "i"}}
        ]
    }
    ergebnisse = list(songs_collection.find(query))
    
    if not ergebnisse:
        print("Keine Songs gefunden.")
        return None
        
    print("\nGefundene Songs:")
    for i, song in enumerate(ergebnisse):
        print(f"[{i}] {song['title']} - {song['artist']} (Album: {song.get('album')})")
        
    wahl = input("\nNummer des gewünschten Songs eingeben (oder Enter zum Abbrechen): ").strip()
    if wahl.isdigit() and 0 <= int(wahl) < len(ergebnisse):
        return ergebnisse[int(wahl)]
    return None

def song_aendern():
    print("\n--- SONG ÄNDERN ---")
    song = song_suchen_und_waehlen()
    if not song:
        print("Abgebrochen oder kein Song gewählt.")
        return
        
    print(f"\nBearbeite: {song['title']} von {song['artist']}")
    neuer_titel = input(f"Neuer Titel [{song['title']}]: ").strip() or song['title']
    neuer_interpret = input(f"Neuer Interpret [{song['artist']}]: ").strip() or song['artist']
    neues_album = input(f"Neues Album [{song.get('album')}]: ").strip() or song.get('album')
    neues_genre = input(f"Neues Genre [{song.get('genre')}]: ").strip() or song.get('genre')
    
    year_input = input(f"Neues Jahr [{song.get('year')}]: ").strip()
    neues_jahr = int(year_input) if year_input.isdigit() else song.get('year')

    songs_collection.update_one(
        {"_id": song["_id"]},
        {"$set": {
            "title": neuer_titel,
            "artist": neuer_interpret,
            "album": neues_album,
            "genre": neues_genre,
            "year": neues_jahr
        }}
    )
    print("Song erfolgreich aktualisiert!")

def song_loeschen():
    print("\n--- SONG LÖSCHEN ---")
    song = song_suchen_und_waehlen()
    if not song:
        print("Abgebrochen.")
        return
        
    bestaetigung = input(f"Möchtest du '{song['title']}' wirklich löschen? (ja/nein): ").strip().lower()
    if bestaetigung == 'ja':
        if song.get("file_id"):
            try:
                bucket.delete(song["file_id"])
                print("Zugehörige Audio-Datei gelöscht.")
            except Exception:
                print("Audio-Datei war in GridFS nicht auffindbar.")
                
        songs_collection.delete_one({"_id": song["_id"]})
        print("Song-Eintrag erfolgreich gelöscht!")

def main():
    while True:
        print("\n=== JUKEBOX MANAGEMENT ===")
        print("[1] Song hinzufügen")
        print("[2] Song ändern")
        print("[3] Song löschen")
        print("[4] Beenden")
        auswahl = input("Auswahl: ").strip()
        
        if auswahl == "1": song_hinzufuegen()
        elif auswahl == "2": song_aendern()
        elif auswahl == "3": song_loeschen()
        elif auswahl == "4": sys.exit()

if __name__ == "__main__":
    main()