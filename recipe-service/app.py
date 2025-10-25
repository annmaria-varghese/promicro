from flask import Flask, request, jsonify
from uuid import uuid4
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

DATA_FILE = "/app/data/recipes.json"
os.makedirs("/app/data", exist_ok=True)

# Load existing data
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        recipes = json.load(f)
else:
    recipes = {}

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(recipes, f)

@app.route("/")
def home():
    return "Recipe Service is running!"

@app.route("/recipes", methods=["GET"])
def get_recipes():
    return jsonify(list(recipes.values()))

@app.route("/recipes/<recipe_id>", methods=["GET"])
def get_recipe(recipe_id):
    return jsonify(recipes.get(recipe_id, {"error":"Recipe not found"}))

@app.route("/recipes", methods=["POST"])
def add_recipe():
    data = request.get_json()
    recipe_id = str(uuid4())
    recipe = {"id": recipe_id, "name": data.get("name"), "instructions": data.get("instructions")}
    recipes[recipe_id] = recipe
    save_data()
    return jsonify(recipe), 201

@app.route("/recipes/<recipe_id>", methods=["PUT"])
def update_recipe(recipe_id):
    if recipe_id not in recipes:
        return jsonify({"error":"Recipe not found"}),404
    data = request.get_json()
    recipes[recipe_id]["name"] = data.get("name")
    recipes[recipe_id]["instructions"] = data.get("instructions")
    save_data()
    return jsonify(recipes[recipe_id])

@app.route("/recipes/<recipe_id>", methods=["DELETE"])
def delete_recipe(recipe_id):
    if recipe_id in recipes:
        recipes.pop(recipe_id)
        save_data()
        return jsonify({"status":"deleted"})
    return jsonify({"error":"Recipe not found"}),404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
