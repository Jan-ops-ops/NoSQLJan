from pymongo import MongoClient


connection_string = "mongodb://localhost:27017/"
client = MongoClient(connection_string)
db = client['Restaurantdb']
collection = db['restaurants']


print("NEUES RESTAURANT HINZUFÜGEN")



def eingabe_mit_validierung(prompt, min_laenge=None, exakte_laenge=None, pflicht=True):
    while True:
        wert = input(prompt).strip()
        
    
        if not pflicht and not wert:
            return ""
            
      
        if pflicht and not wert:
            print("Dies ist ein Pflichtfeld.")
            continue
            
        # Validierung: Mindestlänge prüfen
        if min_laenge and len(wert) < min_laenge:
            print(f"Die Eingabe muss mindestens {min_laenge}lang sein.")
            continue
            
     
        if exakte_laenge and len(wert) != exakte_laenge:
            print(f"Die Eingabe muss exakt {exakte_laenge}lang sein.")
            continue
            
        return wert


name = eingabe_mit_validierung("Name des Restaurants (Pflicht): ", min_laenge=2)
borough = eingabe_mit_validierung("Bezirk / Borough (Pflicht): ", min_laenge=2)
cuisine = eingabe_mit_validierung("Küche / Cuisine (Pflicht): ", min_laenge=2)


building = eingabe_mit_validierung("Hausnummer (Optional): ", pflicht=False)


street = eingabe_mit_validierung("Strasse (Pflicht): ", min_laenge=2)


zipcode = eingabe_mit_validierung("Postleitzahl (Pflicht, exakt 5 Zeichen): ", exakte_laenge=5)



neues_restaurant = {
    "name": name,
    "borough": borough,
    "cuisine": cuisine,
    "address": {
        "building": building,
        "street": street,
        "zipcode": zipcode,
        "coord": [] 
    },
    "grades": []  
}

try:
    ergebnis = collection.insert_one(neues_restaurant)
    print("🎉 [Erfolg] Restaurant erfolgreich gespeichert!")
except Exception as e:
    print(f"\nFehler: {e}")