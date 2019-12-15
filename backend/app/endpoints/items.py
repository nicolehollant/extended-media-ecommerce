from . import routes
from app.config import routes, client, jsonify, request, validate_email, require_fields, empty_fields_response, bad_insert_response, success_response, bad_criteria_response, bad_update_response, bad_delete_response
import random

num_avatars = 5

@routes.route('/items/', methods=["GET"])
def get_items():
  """
  returns all documents in item collection
  """
  res = list(map(lambda x: {
      "name": x["name"],
      "description": x["description"],
      "date": x["date"],
      "paths": x["paths"]
    }, 
    client.find_all("items")))
  return jsonify({
    "message": "Success!",
    "data": res
  }), 200

@routes.route('/items/', methods=["POST"])
def add_item():
  """
  inserts new document in item collection
  
  takes a document like this: 
  {
    "password":    string,      (password that must match email (doesn't get added))
    "email":       string,      (email (convert to _id string in database))
    "name":        string,      (must be at least 1 character)
    "description": string,      (must be at least 1 character)
    "date":        string,      (an int corresponding to the avatar)
    "paths":       list,        (a list of paths - must be at least 1 item)
  }
  """
  reqbody = request.get_json()
  all_present, present, empty_fields = require_fields(reqbody, ["password", "email", "name", "description", "date", "paths"])

  if not all_present:
    return empty_fields_response(empty_fields)

  user = client.find_one({"email": present["email"]}, "users")
  if user["password"] != present.pop("password"): #slick moves popping here :schmile:
    return bad_criteria_response("Password does not match email")

  present["owner_id"] = user["_id"]
  present["reviews"] = []

  print(present["owner_id"]) #pls work

  if len(present["name"]) < 1:
    return bad_criteria_response("name must be > 1 characters")
  if len(present["description"]) < 1:
    return bad_criteria_response("description must be > 1 characters")
  if len(present["date"]) < 1:
    return bad_criteria_response("date must be > 1 characters")
  if len(present["paths"]) < 1:
    return bad_criteria_response("paths must be have at least one item")

  success = client.insert_one(present, "items", criteria=["name"])

  if not success:
    return bad_insert_response()

  return success_response(created=True)

@routes.route('/items/', methods=["PUT"])
def update_item():
  """
  updates existing document in item collection
  
  takes a document like this: 
  {
    "password":    string,      (password that must match email (doesn't get added))
    "email":       string,      (email (convert to _id string in database))
    "name":        string,      (must be at least 1 character)
    "new_name":    string,      (must be at least 1 character)
    "description": string,      (must be at least 1 character)
    "date":        string,      (an int corresponding to the avatar)
    "paths":       list,        (a list of paths - must be at least 1 item)
    "reviews":     list,        (a list of reviews - must be at least 1 item)
  }
  """
  reqbody = request.get_json()
  all_present, present, empty_fields = require_fields(reqbody, ["password", "email", "name"])

  if not all_present:
    return empty_fields_response(empty_fields)

  user = client.find_one({"email": present["email"]}, "users")
  if user["password"] != present.pop("password"):
    return bad_criteria_response("Password does not match email")

  present["owner_id"] = user["_id"]

  item = client.check_exists({"name": present["name"]}, "items")
  if not item:
    return bad_criteria_response("Item does not already exist")

  item = client.find_one({"name": present["name"]}, "items")
  if item["owner_id"] != present["owner_id"]:
    return bad_criteria_response("User doesn't match item owner")
  
  changes = {}
  if reqbody.get("new_name", None):
    changes["name"] = reqbody.get("new_name")
    if len(changes["name"]) < 1:
      return bad_criteria_response("name must be > 1 characters")
  if reqbody.get("description", None):
    changes["description"] = reqbody.get("description")
    if len(changes["description"]) < 1:
      return bad_criteria_response("description must be > 1 characters")
  if reqbody.get("date", None):
    changes["date"] = reqbody.get("date")
    if len(changes["date"]) < 1:
      return bad_criteria_response("date must be > 1 characters")
  if reqbody.get("paths", None):
    changes["paths"] = reqbody.get("paths")
    if len(changes["paths"]) < 1:
      return bad_criteria_response("paths must have at least one item")
  if reqbody.get("reviews", None):
    changes["reviews"] = reqbody.get("reviews")
    for review in changes["reviews"]:
      all_present, _, empty_fields = require_fields(review, ["user", "rating", "comment"])
      if not all_present:
        return empty_fields_response(empty_fields)

  print("\n\nCHANGES\n\n", changes)

  update_result = client.update_one({"name": present["name"]}, changes, "items")

  if update_result['n'] != 1:
    return bad_update_response()

  return success_response(created=True)

@routes.route('/items/', methods=["DELETE"])
def delete_item():
  """
  removes existing document in item collection
  
  takes an obj like this: 
  {
    "email": string,      (key to fetch existing item)
    "password": string,   (validator!)
    "name": string,       (name of item)
  }
  """
  reqbody = request.get_json()
  all_present, present, empty_fields = require_fields(reqbody, ["email", "password", "name"])
  
  if not all_present:
    return empty_fields_response(empty_fields)

  user = client.find_one({"email": present["email"]}, "users")
  if user["password"] != present.pop("password"):
    return bad_criteria_response("Password does not match email")

  present["owner_id"] = user["_id"]

  item = client.find_one({"name": present["name"]}, "items")
  if item["owner_id"] != present["owner_id"]:
    return bad_criteria_response("User doesn't match item owner")

  delete_result = client.delete_one({"name": present["name"]}, "items")

  if delete_result['n'] != 1:
    return bad_delete_response()

  return success_response()

@routes.route('/items/review/', methods=["PUT"])
def add_review():
  """
  adds a review to an existing document in item collection
  
  takes a document like this: 
  {
    "name":        string,      (name of item)
    "email":       string,      (email of user)
    "password":    string,      (password of user)
    "rating":      string,      (rating out of 5)
    "comment":     string,      (comment to display)
    "date":        string,      (date to display)
  }
  """
  reqbody = request.get_json()
  all_present, present, empty_fields = require_fields(reqbody, ["password", "email", "comment", "rating", "date", "name"])

  if not all_present:
    return empty_fields_response(empty_fields)

  if not client.check_exists({"email": present["email"]}, "users"):
    return bad_criteria_response("User does not already exist")
  
  item = client.find_one({"name": present["name"]}, "items")
  if not item:
    return bad_criteria_response("Item does not already exist")
  
  user = client.find_one({"email": present.pop("email")}, "users")
  if user["password"] != present.pop("password"):
    return bad_criteria_response("Password does not match email")


  if len(present["comment"]) < 1:
    return bad_criteria_response("comment must be > 1 characters")
  if len(present["date"]) < 1:
    return bad_criteria_response("date must be > 1 characters")
  try:
    present["rating"] = float(present["rating"]) % 5.1
  except:
    return bad_criteria_response("rating not a number")

  reviews = item["reviews"]
  current = {
    "rating": present["rating"],
    "comment": present["comment"],
    "date": present["date"],
    "user_id": user["_id"]
  }
  reviews.append(current)
  changes = { "reviews": reviews }
  
  update_result = client.update_one({"name": present["name"]}, changes, "items")

  if update_result['n'] != 1:
    return bad_update_response()

  return success_response(created=True)

@routes.route('/items/<name>', methods=["GET"])
def get_item(name):
  """
  returns all info for item
  """
  print(name, request.args, request.view_args["name"])
  item = client.find_one({"name": name}, "items")
  if not item:
    return bad_criteria_response("Item does not already exist")
  reviews = item["reviews"]
  res_reviews = []
  for review in reviews:
    username = "anonymous"
    avatar = random.randint(0, num_avatars)
    user = client.find_one({"_id": review["user_id"]}, "users")
    if user:
      username = user["username"]
      avatar = user["avatar"]

    current = {
      "rating": review["rating"],
      "comment": review["comment"],
      "date": review["date"],
      "username": username,
      "avatar": avatar
    }
    res_reviews.append(current)

  res = item
  res.pop("_id")
  res.pop("owner_id")
  res["reviews"] = res_reviews
  print("\n\nRES\n\n:", res)
  return jsonify({
    "message": "Success!",
    "data": res
  }), 200