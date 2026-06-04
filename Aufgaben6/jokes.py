from pymongo import MongoClient
from bson.objectid import ObjectId

class Joke:
    def __init__(self, text, category, author, joke_id=None):
        self.id = joke_id
        self.text = text
        self.category = category if isinstance(category, list) else [category]
        self.author = author

    def to_dict(self):
        return {
            "text": self.text,
            "category": self.category,
            "author": self.author
        }


class Dao_joke:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.col = MongoClient(connection_string)["jokes_db"]["jokes"]

    def insert(self, joke):
        result = self.col.insert_one(joke.to_dict())
        joke.id = result.inserted_id
        return str(joke.id)

    def get_category(self, category_name):
        query = {"category": category_name}
        results = self.col.find(query)
        
        joke_list = []
        for doc in results:
            joke_list.append(Joke(
                text=doc.get("text"),
                category=doc.get("category"),
                author=doc.get("author"),
                joke_id=str(doc.get("_id"))
            ))
        return joke_list

    def delete(self, joke_id):
        result = self.col.delete_one({"_id": ObjectId(joke_id)})
        return result.deleted_count > 0