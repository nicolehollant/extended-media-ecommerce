import os
import urllib3
import requests 
import json
from pprint import pprint
import datetime

import random

url = "http://localhost:5000/"

items_path = './frontend/src/assets/items.json'
headers = {
  'Content-Type': 'application/json', 
  'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0',
}

def post_items():
  with open(items_path) as f:
    data = json.load(f)["items"]
    for entry in data:
      review_list = entry.pop("reviews")
      # add_item(entry["name"], entry["description"], entry["date"], entry["paths"])
      for review in review_list:
        new_user = {
          "username": review["user"],
          "password": "testpassword",
          "email": review["user"][:].replace(' ', '').replace('-', '') + "@testemail.dev",
          "avatar": random.randint(0, 4)
        }
        # add_user(new_user)
        # print(new_user)
        add_review(entry["name"], new_user["password"], new_user["email"], review["rating"], review["comment"])

def add_user(payload):
  res = requests.post(url + "users/", headers=headers, data=json.dumps(payload))
  print(res)

def add_item(item_name, description, date, paths):
  payload = {
    "password": "nicepassword",
    "email": "coleghollant@gmail.com",
    "name": item_name,
    "description": description,
    "date": date,
    "paths": paths
  }
  res = requests.post(url + "items/", headers=headers, data=json.dumps(payload))
  print(res)

def add_review(item_name, password, email, rating, comment):
  payload = {
    "name": item_name,
    "password": password,
    "email": email,
    "rating": rating,
    "date": str(datetime.datetime.now()),
    "comment": comment
  }
  res = requests.put(url + "items/review/", headers=headers, data=json.dumps(payload))
  print(res, res.text)

if __name__ == "__main__":
  post_items()
    