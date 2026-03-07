# app.api.books

import logging
import os
from dotenv import load_dotenv
import bson
from flask import Blueprint, jsonify, request
from pymongo import MongoClient

load_dotenv()

api = Blueprint("api", __name__, url_prefix="/api")


database_url = os.getenv("DATABASE_URL")
secret_key = os.getenv("SECRET_KEY")
debug_mode = os.getenv("DEBUG_MODE", "False").lower() == "true"

if not database_url:
    raise ValueError("DATABASE_URL is not set")

api.secret_key = secret_key
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

try:
    client = MongoClient(database_url, serverSelectionTimeoutMS=5000)
    client.server_info()  # Force connection
    logging.info("MongoDB connected successfully")
except Exception as e:
    logging.info("Unable to connect with MongoDB:\n{e}")

db = client["bookdb"]
books_collection = db["books"]

# Index
@api.route("/")
def index():
    return jsonify({
        "msg":"Book Management API is Running."
        }), 200

# List all books
@api.route('/books/list/', methods=["GET"])
def books_list():
    result = []
    for book in books_collection.find():
        book["_id"] = str(book["_id"]) # convert the ObjectId to its string representation or Conversely
        result.append(book)
    if len(result) == 0:
        return jsonify({"msg":"No books are in database!"})
    return jsonify(result)

# Add a book
@api.route('/books/add/', methods=["POST"])
def add_book():
    new_book = request.get_json()
    try:
        if new_book:
            books_collection.insert_one(new_book)
            return jsonify({"msg":"Book added Successfully!"}), 201
    except Exception as e:
        return jsonify({"msg": f"Problem while adding book record: {e}"}), 500
    return jsonify({"msg":"Invalid Request!"}), 400

@api.route("/books/<id>/", methods=["GET"])
def book_detail(id):
    if not bson.ObjectId.is_valid(id):
        return jsonify({"error": "Invalid book Id"}), 400

    item_id = bson.ObjectId(id)

    try:
        book_details = books_collection.find_one({"_id": item_id})

        if not book_details:
            return jsonify({"msg": "Book not found"}), 404

        # Convert ObjectId to string for JSON
        book_details["_id"] = str(book_details["_id"])

        return jsonify({"msg": "Book found!", "data": book_details}), 200

    except Exception as e:
        return jsonify({"msg": "Book searching failed", "error": str(e)}), 500

# Update a book
@api.route('/books/<id>/update/', methods=["PATCH"])
def update_book(id):

    if not bson.ObjectId.is_valid(id):
        return jsonify({"error": "Invalid book ID"}), 400

    item_id = bson.ObjectId(id)

    itm = books_collection.find_one({"_id": item_id})
    if not itm:
        return jsonify({"error": "Book not found"}), 404

    if request.method == "PATCH":
        updated_data = request.json
        result = books_collection.update_one(
            {"_id": item_id},
            {"$set": updated_data}
        )

        if result.modified_count > 0:
            return jsonify({"message": "Item updated successfully", "status": "success"}), 200
        else:
            return jsonify({"message": "No changes made", "status": "info"}), 200

    itm["_id"] = str(itm["_id"])  # convert before returning
    return jsonify(itm)

# Delete a book by Id
@api.route('/books/<id>/delete/', methods=["DELETE"])
def delete_book(id):
    if not bson.ObjectId.is_valid(id):
        return jsonify({"error": "Invalid book ID"}), 400

    item_id = bson.ObjectId(id)
    book = books_collection.find_one({"_id": item_id})

    if not book:
        return jsonify({"error": "Book not found"}), 404

    try:
        del_res = books_collection.delete_one({"_id": item_id})
        if del_res.deleted_count == 1:
            book["_id"] = str(book["_id"])  # Convert ObjectId to string
            return jsonify({
                "is_deleted": True,
                "deleted_book": book
            }), 200
        else:
            return jsonify({"error": "Record not found or already deleted"}), 404
    except Exception as e:
        return jsonify({"error": f"Error while deleting record: {e}"}), 500
