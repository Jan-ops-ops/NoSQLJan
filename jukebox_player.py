import sys
import os
import webbrowser
import time
from pymongo import MongoClient
import gridfs

client = MongoClient("mongodb://localhost:27017/")
db = client["jukebox_db"]
songs_collection = db["songs"]
bucket = gridfs.GridFSBucket(db, bucket_name="audio_tracks")

playlist = []

def song_suchen():
    print("\n--- ERWEITERTE SUCHE ---")
    print("Drücke Enter bei Feldern, nach denen du nicht filtern willst.")
    titel = input("Suche nach Titel: ").strip()
    interpret = input("Suche nach Interpret: ").strip()
    album = input("Suche nach Album: ").strip()
    genre = input("Suche nach Genre: ").strip()
    query = {}
    
    if titel:
        query["title"] = {"$regex": titel, "$options": "i"}
    if interpret:
        query["artist"] = {"$regex": interpret, "$options": "i"}
    if album:
        query["album"] = {"$regex": album, "$options": "i"}
    if genre:
        query["genre"] = {"$regex": genre, "$options": "i"}

    ergebnisse = list(songs_collection.find(query))
    return ergebnisse

def song_zu_playlist_hinzufuegen():
    ergebnisse = song_suchen()
    if not ergebnisse:
        print("Keine passenden Songs gefunden.")
        return

    print("\nSuchergebnisse:")
    for i, song in enumerate(ergebnisse):
        print(f"[{i}] {song['title']} - {song['artist']} (Album: {song.get('album', '-')})")

    wahl = input("\nWelcher Song soll in die Playlist? (Nummer eingeben): ").strip()
    if wahl.isdigit() and 0 <= int(wahl) < len(ergebnisse):
        gewaehlter_song = ergebnisse[int(wahl)]
        playlist.append(gewaehlter_song)
        print(f"'{gewaehlter_song['title']}' wurde am Ende der Playlist hinzugefügt.")
    else:
        print("Ungültige Auswahl.")

def playlist_anzeigen():
    print("\n--- AKTUELLE PLAYLIST ---")
    if not playlist:
        print("(Die Playlist ist aktuell leer. Beim Abspielen wird ein Zufallssong gewählt!)")
        return
    for i, song in enumerate(playlist):
        print(f"{i+1}. {song['title']} - {song['artist']}")

def song_abspielen_binaer(song):
    """Simuliert oder startet das Abspielen der Audio-Datei aus GridFS."""
    print(f"\n▶️ Spiele jetzt: '{song['title']}' von '{song['artist']}'")
    
    if song.get("file_id"):
        temp_filename = f"temp_{song['title'].replace(' ', '_')}.mp3"
        try:
            with open(temp_filename, "wb") as f:
                bucket.download_to_stream(song["file_id"], f)
            
            webbrowser.open(temp_filename)
            print("Musik läuft im Hintergrund...")
            time.sleep(2)
        except Exception as e:
            print(f"[Audio-Fehler] Konnte Datei nicht abspielen, Simuliere Track...")
    else:
        print("(Keine Audio-Datei hinterlegt – Track wird nur simuliert...)")
        time.sleep(3)

def naechsten_song_spielen():
    global playlist
    print("\n--- PLAYER ---")
    
    if len(playlist) > 0:
        naechster_song = playlist.pop(0)
        song_abspielen_binaer(naechster_song)
    else:
        print("Playlist ist leer. Hole einen zufälligen Track aus der Datenbank...")
        zufalls_pipeline = [{"$sample": {"size": 1}}]
        zufalls_ergebnis = list(songs_collection.aggregate(zufalls_pipeline))
        
        if zufalls_ergebnis:
            song_abspielen_binaer(zufalls_ergebnis[0])
        else:
            print("Die Musikdatenbank ist komplett leer! Bitte füge erst Songs im Management hinzu.")

def main():
    while True:
        print("\n=== JUKEBOX PLAYER ===")
        print(f"Songs in Warteschlange: {len(playlist)}")
        print("[1] Song suchen & zur Playlist hinzufügen")
        print("[2] Playlist anzeigen")
        print("[3] Nächsten Song abspielen (FIFO / Random)")
        print("[4] Beenden")
        auswahl = input("Auswahl: ").strip()
        
        if auswahl == "1": song_zu_playlist_hinzufuegen()
        elif auswahl == "2": playlist_anzeigen()
        elif auswahl == "3": naechsten_song_spielen()
        elif auswahl == "4": sys.exit()

if __name__ == "__main__":
    main()