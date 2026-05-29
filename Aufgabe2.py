from pymongo import MongoClient
import bson

connection_string = "mongodb://localhost:27017/"
client = MongoClient(connection_string)

def selection():
    dblist = client.list_database_names()
    if not dblist:
        print("No Database") 
        return

    for db_item in dblist:
        print("-", db_item)

    while True:
        print("Select Database:")
        dbname = input()
        if dbname in dblist:
            db = client[dbname]
            break
        else:
            print("Database not found. Please choose again.")

    collist = db.list_collection_names()
    if not collist:
        print("No Collection") 
        return

    print("Collections")
    for col_item in collist:
        print("-", col_item)

    while True:
        print("Select Collection:")
        colname = input()
        if colname in collist:
            col = db[colname]
            break
        else:
            print("Collection not found. Please choose again.")


    docs = list(col.find({}, {"_id": 1}))
    if not docs:
        print("No Document")
        return

    print(dbname, " ", colname)
    print("Documents")
    for doc in docs:
        print("- ID:", doc["_id"])

    while True:
        print("Select Document:")
        docname = input()
        
        try:
            id = bson.ObjectId(docname)
            module = col.find_one({"_id": id})
            
            if module:
                print(dbname, " ", colname, " ", docname)
                for key, value in module.items():
                    print(str(key) + " : " + str(value))
                break
            else:
                print("Document not found. Please choose again.")
        except:
            print("Document not found (Invalid ID). Please choose again.")

while True:
    selection()
    print("\nPress enter to return to the start")
    input()