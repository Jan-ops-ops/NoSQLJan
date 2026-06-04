import sys
from pymongo import MongoClient
from PIL import Image, ImageDraw

client = MongoClient("mongodb://localhost:27017/")

db = client["Restaurantdb"]

collections = db.list_collection_names()
target_collection = None

for col in collections:
    if col.lower() == "neighborhoods":
        target_collection = col
        break

if not target_collection:
    print("--- FEHLER ---")
    print(f"Die Datenbank 'Restaurantdb' wurde gefunden, aber sie enthält keine 'neighborhoods' Collection.")
    print(f"Vorhandene Collections: {collections}")
    sys.exit()

collection = db[target_collection]

neighborhood = collection.find_one()
if not neighborhood:
    print(f"Fehler: Die Collection '{target_collection}' ist komplett leer!")
    sys.exit()

try:
    polygon_coords = neighborhood["geometry"]["coordinates"][0]
except KeyError:
    print("Das gefundene Dokument hat keine gültige GeoJSON-Struktur (geometry.coordinates).")
    sys.exit()

x_coords = [p[0] for p in polygon_coords]
y_coords = [p[1] for p in polygon_coords]

min_x, max_x = min(x_coords), max(x_coords)
min_y, max_y = min(y_coords), max(y_coords)


img_w, img_h = 800, 800
padding = 50  


def to_pixel(lon, lat):
  
    x_pct = (lon - min_x) / (max_x - min_x) if (max_x - min_x) > 0 else 0.5
    # Y-Achse umdrehen, da bei Bildern '0' oben ist
    y_pct = 1.0 - ((lat - min_y) / (max_y - min_y) if (max_y - min_y) > 0 else 0.5)
    
    pixel_x = padding + x_pct * (img_w - 2 * padding)
    pixel_y = padding + y_pct * (img_h - 2 * padding)
    return (pixel_x, pixel_y)

pixel_points = [to_pixel(p[0], p[1]) for p in polygon_coords]

im = Image.new(mode="RGB", size=(img_w, img_h), color=(10, 10, 20))
draw = ImageDraw.Draw(im)

draw.polygon(pixel_points, outline=(0, 255, 255), fill=(30, 60, 100))

print(f"Erfolg! Zeichne Nachbarschaft: '{neighborhood.get('name', 'Unbekannt')}'")
im.show()