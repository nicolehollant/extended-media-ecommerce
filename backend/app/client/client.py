import flask_pymongo
import pymongo

class Client():
  """
  Database client!
  - TODO: big problem, never should access collection and query inline
          instead, please, please, check existence of collection first
  """

  def __init__(self, uri=None, dbname=None):
    if not uri:
      uri = "mongodb://localhost:27017"
    if not dbname:
      dbname = "testdb"
    self.uri = uri
    self.dbname = dbname
    self.client = pymongo.MongoClient(self.uri)
    self.db = self.client[self.dbname]
    self.collections = {}

  def get_collections(self):
    return self.collections

  def add_collection(self, collection_name):
    self.collections[collection_name] = self.db[collection_name]
    return self.collections[collection_name]

  def get_collection(self, collection_name):
    return self.collections[collection_name]

  def insert_one(self, insert, collection_name, criteria=None):
    """
    inserts [insert] to [collection_name]
    - [criteria] is a list of keys to consider
    returns success status
    """
    
    check = {}
    if criteria:
      for c in criteria:
        if insert.get(c, False):
          check[c] = insert[c]

    if criteria and self.check_exists(check, collection_name):
      print(f"Item exists: {insert}")
      return False
    try:
      self.collections[collection_name].insert_one(insert)
      print(f"Added item: {insert}")
      return True
    except:
      print(f"Failed to add item: {insert}")
      return False


  def insert_many(self, insert, collection_name, criteria=None):
    """
    inserts all of [insert] to [collection_name]
    - [criteria] is a list of keys to consider
    returns success status
    """
    return [self.insert_one(item, collection_name, criteria) for item in insert]
  
  def find_all(self, collection_name):
    return list(self.collections[collection_name].find())
  
  def find(self, search_filter, collection_name):
    return list(self.collections[collection_name].find({}, search_filter))

  def find_one(self, search_filter, collection_name):
    return self.collections[collection_name].find_one(search_filter)

  def check_exists(self, search_filter, collection_name):
    """
    returns whether anything in the collection matches the search criteria
    """
    return self.find_one(search_filter, collection_name) != None
  
  def delete_many(self, search_filter, collection_name):
    res = self.collections[collection_name].delete_many(search_filter)
    return res.raw_result

  def delete_one(self, search_filter, collection_name):
    return self.collections[collection_name].delete_one(search_filter).raw_result
  
  def update_one(self, search_filter, update, collection_name):
    return self.collections[collection_name].update_one(search_filter, { "$set": update }).raw_result

  @staticmethod
  def test_ops(client):
    mydict = { "name": "John", "address": "Highway 37" }
    mylist = [
      { "name": "Amy", "address": "Apple st 652"},
      { "name": "Hannah", "address": "Mountain 21"},
      { "name": "Hannah", "address": "Mountain 22"},
      { "name": "Hannah", "address": "Mountain 23"},
      { "name": "Michael", "address": "Valley 345"},
      { "name": "Sandy", "address": "Ocean blvd 2"},
      { "name": "Betty", "address": "Green Grass 1"},
      { "name": "Richard", "address": "Sky st 331"},
      { "name": "Susan", "address": "One way 98"},
      { "name": "Vicky", "address": "Yellow Garden 2"},
      { "name": "Ben", "address": "Park Lane 38"},
      { "name": "William", "address": "Central st 954"},
      { "name": "Chuck", "address": "Main Road 989"},
      { "name": "Viola", "address": "Sideway 1633"}
    ]

    criteria = ["name", "address"]
    client.add_collection("test")
    client.insert_one(mydict, "test", criteria=criteria)
    client.insert_many(mylist, "test", criteria=criteria)

    print(client.find_all("test"))
    print(client.find_one({"name": "Ben"}, "test"))
    print(client.check_exists({"name": "Beasdn"}, "test"))

    print(client.delete_one({"name": "Ben"}, "test"))
    print(client.delete_many({"name": "Hannah"}, "test"))
    print(client.update_one({"name": "Amydd"}, {"name": "WoaaaahAmy"}, "test"))