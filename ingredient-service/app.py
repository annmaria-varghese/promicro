from flask import Flask, request, jsonify
from uuid import uuid4
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

DATA_FILE = "/app/data/ingredients.json"
os.makedirs("/app/data", exist_ok=True)

# Load existing data
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        ingredients = json.load(f)
else:
    ingredients = {}

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(ingredients, f)

@app.route("/")
def home():
    return "Ingredient Service is running!"

@app.route("/ingredients", methods=["GET"])
def get_ingredients():
    return jsonify(list(ingredients.values()))

@app.route("/ingredients/<ingredient_id>", methods=["GET"])
def get_ingredient(ingredient_id):
    return jsonify(ingredients.get(ingredient_id, {"error":"Ingredient not found"}))

@app.route("/ingredients", methods=["POST"])
def add_ingredient():
    data = request.get_json()
    ing_id = str(uuid4())
    ing = {"id": ing_id, "name": data.get("name"), "quantity": data.get("quantity")}
    ingredients[ing_id] = ing
    save_data()
    return jsonify(ing), 201

@app.route("/ingredients/<ingredient_id>", methods=["PUT"])
def update_ingredient(ingredient_id):
    if ingredient_id not in ingredients:
        return jsonify({"error":"Ingredient not found"}),404
    data = request.get_json()
    ingredients[ingredient_id]["name"] = data.get("name")
    ingredients[ingredient_id]["quantity"] = data.get("quantity")
    save_data()
    return jsonify(ingredients[ingredient_id])

@app.route("/ingredients/<ingredient_id>", methods=["DELETE"])
def delete_ingredient(ingredient_id):
    if ingredient_id in ingredients:
        ingredients.pop(ingredient_id)
        save_data()
        return jsonify({"status":"deleted"})
    return jsonify({"error":"Ingredient not found"}),404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
