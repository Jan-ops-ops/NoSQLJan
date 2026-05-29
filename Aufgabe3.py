from pymongo import MongoClient, GEOSPHERE

connection_string = "mongodb://localhost:27017/"
client = MongoClient(connection_string)
db = client['Restaurantdb']
collection = db['restaurants']

#3.1
diffBorough = collection.distinct("borough")

for borogh in diffBorough :

    print(borogh)


#3.2

pipeline = [
    {"$unwind": "$grades"},
    
    {"$group": {
        "_id": "$name", 
        "averageScore": {"$avg": "$grades.score"}
    }},
    
    {"$sort": {"averageScore": -1}},
    
    {"$limit": 3}
]
top_restaurants = list(collection.aggregate(pipeline))
for res in top_restaurants:
    print(f"Restaurant: {res['_id']} | Score: {res['averageScore']:.2f}")

#3.3

collection.create_index([("address.coord", GEOSPHERE)])
start_restaurant = collection.find_one({"name": "Le Perigord"})
cords = start_restaurant.get("address", {}).get("coord")

query = {
    "_id": {"$ne": start_restaurant["_id"]},
    "address.coord": {
        "$near": {
            "$geometry": {
                "type": "Point",
                "coordinates": cords
            }
        }
    }
}

naechstes_restaurant = collection.find_one(query)
if naechstes_restaurant:
        print(f"Das nächste Restaurant ist: {naechstes_restaurant['name']}")
        print(naechstes_restaurant["address"]["coord"])



#