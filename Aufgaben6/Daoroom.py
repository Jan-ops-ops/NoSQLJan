from pymongo import MongoClient
from bson.objectid import ObjectId
from room import Room

class Dao_room:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.col = MongoClient(connection_string)["buildings"]["rooms"]

    def create(self, room):
        self.col.insert_one(room.__dict__)

    def read(self):
        room = Room(**self.col.find_one())
        return room

    def update(self, room_id, update_data):
        result = self.col.update_one(
            {"_id": ObjectId(room_id)}, 
            {"$set": update_data}
        )
        return result.modified_count > 0

    def delete(self, room_id):
        result = self.col.delete_one({"_id": ObjectId(room_id)})
        return result.deleted_count > 0