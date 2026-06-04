import os
from pymongo import MongoClient
import gridfs
from bson.objectid import ObjectId

client = MongoClient("mongodb://localhost:27017/")
db = client["fotoalbum_db"]


bucket = gridfs.GridFSBucket(db, bucket_name="photos")


def foto_hinzufuegen(dateipfad, album_name):
    """Speichert ein Foto mit dem zugehörigen Album-Namen als Metadaten."""
    if not os.path.exists(dateipfad):
        print(f"Fehler: Datei {dateipfad} existiert nicht.")
        return None

    dateiname = os.path.basename(dateipfad)


    with open(dateipfad, "rb") as f:
        file_id = bucket.upload_from_stream(
            dateiname, f, metadata={"album": album_name}
        )

    print(
        f"Erfolgreich hochgeladen: '{dateiname}' wurde zum Album '{album_name}' hinzugefügt. (ID: {file_id})"
    )
    return file_id


def album_herunterladen(album_name, ziel_ordner="./download"):
    """Sucht alle Fotos eines Albums und lädt sie in einen lokalen Ordner herunter."""
    if not os.path.exists(ziel_ordner):
        os.makedirs(ziel_ordner)


    photos = db["photos.files"].find({"metadata.album": album_name})

    anzahl = 0
    for photo in photos:
        file_id = photo["_id"]
        dateiname = photo["filename"]
        ziel_pfad = os.path.join(ziel_ordner, dateiname)


        with open(ziel_pfad, "wb") as f:
            bucket.download_to_stream(file_id, f)

        print(f"Heruntergeladen: {dateiname} -> {ziel_pfad}")
        anzahl += 1

    if anzahl == 0:
        print(f"Keine Fotos im Album '{album_name}' gefunden.")
    else:
        print(f"Fertig! {anzahl} Foto(s) aus dem Album '{album_name}' heruntergeladen.")



if __name__ == "__main__":

    with open("sommer_sonne.jpg", "wb") as f:
        f.write(b"Hier stehen die Binaerdaten von Bild 1")
    with open("strand.jpg", "wb") as f:
        f.write(b"Hier stehen die Binaerdaten von Bild 2")
    with open("schnee.jpg", "wb") as f:
        f.write(b"Hier stehen die Binaerdaten von Bild 3")

    print("--- 1. Fotos zu Alben hinzufügen ---")
    foto_hinzufuegen("sommer_sonne.jpg", "Urlaub 2026")
    foto_hinzufuegen("strand.jpg", "Urlaub 2026")
    foto_hinzufuegen("schnee.jpg", "Winter 2026")

    print("\n--- 2. Album 'Urlaub 2026' herunterladen ---")
    album_herunterladen("Urlaub 2026", ziel_ordner="./mein_urlaubs_album")

   
    for f in ["sommer_sonne.jpg", "strand.jpg", "schnee.jpg"]:
        if os.path.exists(f):
            os.remove(f)