from . import routes
from app.config import routes, client, jsonify, request, validate_email, require_fields, empty_fields_response, bad_insert_response, success_response, bad_criteria_response, bad_update_response, bad_delete_response, admin_username, admin_password
import datetime

num_avatars = 5

@routes.route('/orders/all/', methods=["POST"])
def get_orders():
  """
  returns all documents in order collection
  """
  reqbody = request.get_json()
  all_present, present, empty_fields = require_fields(reqbody, ["username", "password"])
  if not all_present:
    return empty_fields_response(empty_fields)
  if present["username"] != admin_username or present["password"] != admin_password:
    return bad_criteria_response("Invalid admin creds")

  res = list(map(lambda x: {
      "order": x["order"],
      "email": x["email"],
      "items": x["items"],
    }, 
    client.find_all("orders")))
  return jsonify({
    "message": "Success!",
    "data": res
  }), 200

@routes.route('/orders/', methods=["POST"])
def add_order():
  """
  inserts new document in order collection
  
  takes a document like this: 
  {
    "items": list,        (must be nonempty)
    "password": string,   (must be at least 5 characters)
    "email": string,      (must be an email)
  }
  """
  reqbody = request.get_json()
  all_present, present, empty_fields = require_fields(reqbody, ["items", "password", "email"])
  
  if not all_present:
    return empty_fields_response(empty_fields)
  if not client.check_exists({"email": present["email"]}, "users"):
    return bad_criteria_response("User does not already exist")
  user = client.find_one({"email": present["email"]}, "users")
  if user["password"] != present.pop("password"):
    return bad_criteria_response("Password does not match email")
  # make sure that all the items exist!
  for item in present["items"][:]:
    if not client.check_exists({"name": item}, "items"):
      present["items"].remove(item)
  if len(present["items"]) == 0:
    return bad_criteria_response("No valid items")

  present["order"] = present["email"] + "___" + str(datetime.datetime.now())
  success = client.insert_one(present, "orders", criteria=["order"])

  if not success:
    return bad_insert_response()

  return success_response(created=True)

@routes.route('/orders/', methods=["DELETE"])
def delete_order():
  """
  removes existing document in order collection
  
  takes an obj like this: 
  {
    "username": string,   (admin username)
    "password": string,   (admin password)
    "order": string       (key to fetch existing order)
  }
  """
  reqbody = request.get_json()
  all_present, present, empty_fields = require_fields(reqbody, ["username", "password", "order"])
  
  if not all_present:
    return empty_fields_response(empty_fields)

  if present["username"] != admin_username or present["password"] != admin_password:
    return bad_criteria_response("Invalid admin creds")

  if not client.check_exists({"order": present["order"]}, "orders"):
    return bad_criteria_response("Order does not exist")

  delete_result = client.delete_one({"order": present["order"]}, "orders")

  if delete_result['n'] != 1:
    return bad_delete_response()

  return success_response()