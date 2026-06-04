import sys
from pymongo import MongoClient
from PIL import Image, ImageDraw

client = MongoClient("mongodb://localhost:27017/")
db = client["Restaurantdb"]
collection = db["neighborhoods"]

all_neighborhoods = list(collection.find())
if not all_neighborhoods:
    print("Fehler: Keine Daten in der Collection 'neighborhoods' gefunden!")
    sys.exit()

print(f"Erfolgreich {len(all_neighborhoods)} Stadtviertel geladen. Berechne Karte...")

all_x, all_y = [], []

def extract_points(coords_entry):
    """Hilfsfunktion, die alle [X, Y] Paare findet, egal wie tief sie verschachtelt sind."""
    points = []
    if isinstance(coords_entry, list):
        if len(coords_entry) == 2 and isinstance(coords_entry[0], (int, float)):
            points.append(coords_entry)
        else:
            for sub in coords_entry:
                points.extend(extract_points(sub))
    return points

for n in all_neighborhoods:
    if "geometry" in n and "coordinates" in n["geometry"]:
        raw_coords = n["geometry"]["coordinates"]
        valid_points = extract_points(raw_coords)
        for pt in valid_points:
            all_x.append(pt[0])
            all_y.append(pt[1])

if not all_x:
    print("Fehler: Keine gültigen Koordinaten in den Dokumenten gefunden.")
    sys.exit()

global_min_x, global_max_x = min(all_x), max(all_x)
global_min_y, global_max_y = min(all_y), max(all_y)

img_w, img_h = 1200, 1200
padding = 60

def to_pixel_global(lon, lat):
    x_pct = (lon - global_min_x) / (global_max_x - global_min_x) if (global_max_x - global_min_x) > 0 else 0.5
    y_pct = 1.0 - ((lat - global_min_y) / (global_max_y - global_min_y) if (global_max_y - global_min_y) > 0 else 0.5)
    
    px = padding + x_pct * (img_w - 2 * padding)
    py = padding + y_pct * (img_h - 2 * padding)
    return (px, py)

im = Image.new(mode="RGB", size=(img_w, img_h), color=(15, 15, 25))
draw = ImageDraw.Draw(im)

for n in all_neighborhoods:
    if "geometry" in n and "coordinates" in n["geometry"]:
        raw_coords = n["geometry"]["coordinates"]
        
        def get_rings(data):
            if isinstance(data, list) and len(data) > 0:
                if isinstance(data[0], list) and len(data[0]) == 2 and isinstance(data[0][0], (int, float)):
                    return [data]
                else:
                    rings = []
                    for item in data:
                        rings.extend(get_rings(item))
                    return rings
            return []

        rings = get_rings(raw_coords)
        
        for ring in rings:
            try:
                if len(ring) < 3:
                    continue 
                pixel_points = [to_pixel_global(p[0], p[1]) for p in ring]
              
                draw.polygon(pixel_points, outline=(100, 100, 150), fill=(40, 50, 90))
            except Exception:
                continue

print("Fertig! Karte wird geöffnet...")
im.show()