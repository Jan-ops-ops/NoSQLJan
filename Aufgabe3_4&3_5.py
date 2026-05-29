from pymongo import MongoClient
from datetime import datetime

connection_string = "mongodb://localhost:27017/"
client = MongoClient(connection_string)
db = client['Restaurantdb']
collection = db['restaurants']

print("=" * 45)
print("       RESTAURANT SUCHEN")
print("=" * 45)
print("(Eingabe leer lassen, um das Feld zu ignorieren)\n")

eingabe_name = input("Nach welchem Namen suchen? ").strip()
eingabe_kueche = input("Nach welcher Küche suchen? ").strip()

query = {}

if eingabe_name:
    query["name"] = {"$regex": eingabe_name, "$options": "i"}

if eingabe_kueche:
    query["cuisine"] = {"$regex": eingabe_kueche, "$options": "i"}

ergebnisse = list(collection.find(query))
anzahl = len(ergebnisse)

print("\n" + "=" * 45)
print(f"ERGEBNIS: {anzahl} Restaurant(s) gefunden")
print("=" * 45)

if anzahl > 0:
    for rest in ergebnisse:
        print(f"  {rest.get('name', 'Unbekannt')}")
        print(f"   Küche:  {rest.get('cuisine', 'Unbekannt')}")
        print(f"   Bezirk: {rest.get('borough', 'Unbekannt')}")
        print("-" * 45)
else:
    print("Keine Restaurants entsprechen deinen Suchkriterien.")

selected_id = None

if anzahl == 0:
    print("\nKeine Restaurants gefunden, die diesen Kriterien entsprechen.")
    exit()

print(f"\nFolgende {anzahl} Restaurants entsprechen deiner Suche. Bitte wähle eines aus:")
print("-" * 50)
for index, rest in enumerate(ergebnisse):
    print(f"[{index + 1}] {rest.get('name')} | Bezirk: {rest.get('borough')} | Küche: {rest.get('cuisine')}")
print("-" * 50)

try:
    auswahl = int(input("Nummer des Restaurants eingeben: ")) - 1
    if 0 <= auswahl < anzahl:
        selected_id = ergebnisse[auswahl]["_id"]
        print(f"\nAusgewähltes Restaurant: {ergebnisse[auswahl]['name']}")
    else:
        print("Ungültige Nummer eingegeben.")
        exit()
except ValueError:
    print("Bitte gib eine gültige Zahl ein.")
    exit()

if selected_id:
    print("\n" + "=" * 30)
    print("      BEWERTUNGSMENÜ")
    print("=" * 30)
    
    try:
        score = int(input("Gib deinen Score ein (0 - 100): "))
        if not (0 <= score <= 100):
            print("Fehler: Der Score muss zwischen 0 und 100 liegen!")
            exit()
    except ValueError:
        print("Fehler: Der Score muss eine ganze Zahl sein.")
        exit()
        
   
    grade = input("Gib eine Note/Grad ein (z.B. A, B, C) oder leer lassen: ").strip().upper()
    if not grade:
        grade = "N/A"


    neue_bewertung = {
        "date": datetime.now(),
        "grade": grade,
        "score": score
    }
    
    collection.update_one(
        {"_id": selected_id},
        {"$push": {"grades": neue_bewertung}}
    )
    
    print("\n[Erfolg] Deine Bewertung (Score: {}, Note: {}) wurde gespeichert!".format(score, grade))
