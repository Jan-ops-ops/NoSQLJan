from pymongo import MongoClient

connection_string = "mongodb://localhost:27017/"
client = MongoClient(connection_string)
db = client['Restaurantdb']
collection = db['restaurants']


while True:
    suchbegriff = input("Name oder TeilName eingeben: ").strip()
    if not suchbegriff:
        print("Pflichtfeld.")
        continue
    if len(suchbegriff) < 2:
        print("Fehler: Die Eingabe muss mindestens 2 Zeichen lang sein.")
        continue
    break


query = {"name": {"$regex": suchbegriff, "$options": "i"}}
ergebnisse = list(collection.find(query))
anzahl = len(ergebnisse)


if anzahl == 0:
    print("Es wurden keine Restaurants gefunden.")
else:
    print(f"Es wurden {anzahl} Restaurants gefunden. Bitte auswählen:")
    
   
    for index, rest in enumerate(ergebnisse):
        print(f"[{index + 1}] {rest.get('name')} | Bezirk: {rest.get('borough')} | Küche: {rest.get('cuisine')}")
        
    
    try:
        auswahl = int(input("Nummer Eingeben: ")) - 1
        if 0 <= auswahl < anzahl:
            ausgewaehltes_restaurant = ergebnisse[auswahl]
            selected_id = ausgewaehltes_restaurant["_id"]
            
           
            bestaetigung = input(f"Möchten Sie das Restaurant '{ausgewaehltes_restaurant.get('name')}' löschen? (ja/nein): ").strip().lower()
            
            if bestaetigung == "ja":
                loesch_ergebnis = collection.delete_one({"_id": selected_id})
                print("Das Restaurant wurde gelöscht.")
            else:
                print("Löschen Abgebrochen")
        else:
            print("Ungültige Nummer eingegeben.")
    except ValueError:
        print("Bitte gib eine gültige Zahl ein.")