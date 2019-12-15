import re 
from flask import jsonify


def validate_email(email):
  """
  email validator
  
  params:
  - email: email to validate
  returns:
  - boolean: whether email is valid
  """
  email_regex = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
  if(re.search(email_regex, email)):
    print("Valid Email")
    return True
  else:  
    print("Invalid Email") 
    return False

def require_fields(request_body, required_fields):
  """
  empty field validator
  
  params:
  - request_body: incoming request
  - required_fields: fields that must be present
  returns:
  - whether there are any missing fields
  - field -> value dict
  - list of missing fields
  """
  missing_fields = []
  present = {}
  for field in required_fields:
    if not request_body[field]:
      missing_fields.append(field)
    else:
      present[field] = request_body[field]
  return len(missing_fields) == 0, present, missing_fields

def empty_fields_response(empty_fields):
  """
  empty fields response

  params:
  - empty_fields: list of field names that werent present
  returns:
  - response
  """
  return jsonify({
    "message": "empty fields present in request", 
    "empty_fields": empty_fields
  }), 400

def bad_insert_response():
  """
  bad insert response

  returns:
  - response
  """
  return jsonify({ "message": "failed to insert" }), 400

def bad_update_response():
  """
  bad update response

  returns:
  - response
  """
  return jsonify({ "message": "failed to update" }), 400

def bad_delete_response():
  """
  bad delete response

  returns:
  - response
  """
  return jsonify({ "message": "failed to delete" }), 400

def success_response(created=False):
  """
  success response

  returns:
  - response
  """
  code = 201 if created else 200
  return jsonify({"message": "success!"}), code

def bad_criteria_response(message):
  """
  bad value response
  - if a passed field doesnt meet the criteria

  returns:
  - response
  """
  return jsonify({"message": message}), 400