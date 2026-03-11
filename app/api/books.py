import logging
import os
import bson
from dotenv import load_dotenv
from flask import Blueprint, jsonify, request
from pymongo import MongoClient
from bson import ObjectId, Decimal128

load_dotenv()

api = Blueprint("api", __name__, url_prefix="/api")

# Connect to DB
database_url = os.getenv("DATABASE_URL")
client = MongoClient(database_url, serverSelectionTimeoutMS=5000)
db = client["bookdb"]
books_collection = db["books"]
author_collection = db["authors"]

# Helper to cast types for MongoDB Validation compliance
def cast_book_data(data):
    if 'year' in data and data['year'] is not None:
        data['year'] = int(data['year'])
    if 'price' in data and data['price'] is not None:
        data['price'] = Decimal128(str(data['price']))
    return data

@api.route("/")
def index():
    return jsonify({"msg": "Book Management API is Running."}), 200

# 1. List all books
@api.route('/books/list/', methods=["GET"])
def books_list():
    # list() converts cursor to list; MongoJSONProvider handles the rest
    result = list(books_collection.find())
    if not result:
        return jsonify({"msg": "No books found"}), 204
    return jsonify(result)

# 2. Add a book
@api.route('/books/add/', methods=["POST"])
def add_book():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    try:
        # Cast types so MongoDB validation doesn't reject them
        new_book = cast_book_data(data)
        books_collection.insert_one(new_book)
        return jsonify({"msg": "Book added Successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 3. Book Detail
@api.route("/books/<id>/", methods=["GET"])
def book_detail(id):
    if not ObjectId.is_valid(id):
        return jsonify({"error": "Invalid ID format"}), 400

    book = books_collection.find_one({"_id": ObjectId(id)})
    if not book:
        return jsonify({"msg": "Book not found"}), 404
    return jsonify(book)

# 4. Update a book (PATCH)
@api.route('/books/<id>/update/', methods=["PATCH"])
def update_book(id):
    if not ObjectId.is_valid(id):
        return jsonify({"error": "Invalid ID format"}), 400

    update_data = request.get_json()
    if not update_data:
        return jsonify({"error": "Missing update data"}), 400

    try:
        # Cast types for validation
        clean_data = cast_book_data(update_data)
        result = books_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": clean_data}
        )
        if result.matched_count == 0:
            return jsonify({"error": "Book not found"}), 404
        return jsonify({"message": "Updated", "modified": result.modified_count}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 5. Delete a book
@api.route('/books/<id>/delete/', methods=["DELETE"])
def delete_book(id):
    if not ObjectId.is_valid(id):
        return jsonify({"error": "Invalid ID format"}), 400

    res = books_collection.find_one_and_delete({"_id": ObjectId(id)})
    if not res:
        return jsonify({"error": "Book not found"}), 404
    return jsonify({"is_deleted": True, "deleted_book": res}), 200

# 6. Author info
@api.route('/author/<id>/',methods=["GET"])
def author_info(id):
    if not ObjectId.is_valid(id):
        return jsonify({"error":"Invalid Author id"})
    res = author_collection.find_one({"_id": ObjectId(id)})
    if not res:
        return jsonify({"msg":"no author information found"}), 204
    return jsonify(res),200


# 7. Filter by price
@api.route('/books/price/gt/<num>/', methods=["GET"])
def filter_book_gt(num):
    try:
        # URL parameters are always strings, must convert to Decimal128 for MongoDB
        price_val = Decimal128(str(num))
        results = list(books_collection.find({"price": {"$gte": price_val}}))
        if not results:
            return jsonify([]), 200
        return jsonify(results)
    except Exception:
        return jsonify({"error": "Invalid price format"}), 400
