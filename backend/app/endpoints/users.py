from . import routes
from app.config import routes, client, jsonify, request, validate_email, require_fields, empty_fields_response, bad_insert_response, success_response, bad_criteria_response, bad_update_response, bad_delete_response

num_avatars = 5

@routes.route('/users/', methods=["GET"])
def get_users():
  """
  returns all documents in user collection
  """

  res = list(map(lambda x: {
      "username": x["username"],
      "email": x["email"],
      "avatar": x["avatar"],
    }, 
    client.find_all("users")))
  return jsonify({
    "message": "Success!",
    "data": res
  }), 200

@routes.route('/users/', methods=["POST"])
def add_user():
  """
  inserts new document in user collection
  
  takes a document like this: 
  {
    "username": string,   (must be at least 3 characters)
    "password": string,   (must be at least 5 characters)
    "email": string,      (must be an email)
    "avatar": int,        (an int corresponding to the avatar)
  }
  """
  reqbody = request.get_json()
  all_present, present, empty_fields = require_fields(reqbody, ["username", "password", "email"])
  
  if not all_present:
    return empty_fields_response(empty_fields)

  present["avatar"] = int(reqbody.get("avatar", 0)) % num_avatars

  if len(present["username"]) < 5:
    return bad_criteria_response("Username must be > 5 characters")
  if len(present["password"]) < 5:
    return bad_criteria_response("Password must be > 5 characters")
  if not validate_email(present["email"]):
    return bad_criteria_response("Invalid email")

  success = client.insert_one(present, "users", criteria=["email"])

  if not success:
    return bad_insert_response()

  return success_response(created=True)

@routes.route('/users/', methods=["PUT"])
def update_user():
  """
  updates existing document in user collection
  
  takes a document like this: 
  {
    "email": string,      (key to fetch existing user)
    "username": string,   (must be at least 3 characters)
    "password": string,   (must be at least 5 characters)
    "new_password": string,   (must be at least 5 characters)
    "new_email": string,  (must be an email)
    "avatar": int,        (an int corresponding to the avatar)
  }
  """
  reqbody = request.get_json()
  all_present, present, empty_fields = require_fields(reqbody, ["email", "password"])
  
  if not all_present:
    return empty_fields_response(empty_fields)

  if not client.check_exists({"email": present["email"]}, "users"):
    return bad_criteria_response("User does not already exist")

  user = client.find_one({"email": present["email"]}, "users")
  
  if user["password"] != present["password"]:
    return bad_criteria_response("Password does not match email")  
  
  changes = {}
  if reqbody.get("avatar", None):
    changes["avatar"] = int(reqbody.get("avatar")) % num_avatars
  if reqbody.get("username", None):
    changes["username"] = reqbody.get("username")
    if len(changes["username"]) < 5:
      return bad_criteria_response("Username must be > 5 characters")
  if reqbody.get("new_password", None):
    changes["password"] = reqbody.get("new_password")
    if len(changes["password"]) < 5:
      return bad_criteria_response("Password must be > 5 characters")
  if reqbody.get("new_email", None):
    changes["email"] = reqbody.get("new_email")
    if not validate_email(changes["email"]):
      return bad_criteria_response("Invalid email")

  update_result = client.update_one({"email": present["email"]}, changes, "users")

  if update_result['n'] != 1:
    return bad_update_response()

  return success_response(created=True)

@routes.route('/users/', methods=["DELETE"])
def delete_user():
  """
  removes existing document in user collection
  
  takes an obj like this: 
  {
    "email": string,      (key to fetch existing user)
    "password": string,   (validator!)
  }
  """
  reqbody = request.get_json()
  all_present, present, empty_fields = require_fields(reqbody, ["email", "password"])
  
  if not all_present:
    return empty_fields_response(empty_fields)

  if not client.check_exists({"email": present["email"]}, "users"):
    return bad_criteria_response("User does not already exist")
  user = client.find_one({"email": present["email"]}, "users")
  if user["password"] != present["password"]:
    return bad_criteria_response("Password does not match email")

  delete_result = client.delete_one({"email": present["email"]}, "users")

  if delete_result['n'] != 1:
    return bad_delete_response()

  return success_response()

@routes.route('/users/login/', methods=["POST"])
def get_user():
  """
  log in! (get info for user)
  """
  reqbody = request.get_json()
  all_present, present, empty_fields = require_fields(reqbody, ["email", "password"])
  
  if not all_present:
    return empty_fields_response(empty_fields)

  if not client.check_exists({"email": present["email"]}, "users"):
    return bad_criteria_response("User does not already exist")
  user = client.find_one({"email": present["email"]}, "users")
  if user["password"] != present["password"]:
    return bad_criteria_response("Password does not match email")

  user.pop("_id")

  return jsonify({
    "message": "Success!",
    "data": user
  }), 200