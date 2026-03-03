import os
from bson import ObjectId
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.errors import InvalidId

load_dotenv()
app = Flask(__name__)

database_url = os.getenv("DATABASE_URL")
secret_key = os.getenv("SECRET_KEY")
debug_mode = os.getenv("DEBUG_MODE", "False").lower() == "true"

if not database_url:
    raise ValueError("DATABASE_URL is not set")

app.secret_key = secret_key

try:
    client = MongoClient(database_url, serverSelectionTimeoutMS=5000)
    client.server_info()  # Force connection
    print("Connected to MongoDB successfully")
except Exception as e:
    print("Unable to connect with MongoDB:", e)

db = client["bookdb"]
books_collection = db["books"]

# Index
@app.route("/")
def index():
    return jsonify({
        "msg":"Book Management API is Running."
        }), 200

# List all books
@app.route('/books/list/', methods=["GET"])
def books_list():
    result = []
    for book in books_collection.find():
        book["_id"] = str(book["_id"]) # convert the ObjectId to its string representation or Conversely
        result.append(book)
    if len(result) == 0:
        return jsonify({"msg":"No books are in database!"})
    return jsonify(result)

# Add a book
@app.route('/books/add/', methods=["POST"])
def add_book():
    new_book = request.get_json()
    print("[DEBUG]", new_book)
    try:
        if new_book:
            books_collection.insert_one(new_book)
            return jsonify({"msg":"Book added Successfully!"}), 201
    except Exception as e:
        print("Problem while adding book record", e)
    return jsonify({"msg":"Invalid Request!"}), 400

@app.route("/books/<id>/", methods=["GET"])
def book_detail(id):
    if not ObjectId.is_valid(id):
        return jsonify({"error": "Invalid book Id"}), 400

    item_id = ObjectId(id)

    try:
        book_details = books_collection.find_one({"_id": item_id})

        if not book_details:
            return jsonify({"msg": "Book not found"}), 404

        # Convert ObjectId to string for JSON
        book_details["_id"] = str(book_details["_id"])

        print(f'[DEBUG] BOOK found: \n{book_details}')

        return jsonify({"msg": "Book found!", "data": book_details}), 200

    except Exception as e:
        print(f"[DEBUG] Book searching failed due to: {e}")
        return jsonify({"msg": "Book searching failed", "error": str(e)}), 500

# Update a book
@app.route('/books/<id>/update/', methods=["GET", "PUT"])
def update_book(id):

    if not ObjectId.is_valid(id):
        return jsonify({"error": "Invalid book ID"}), 400

    item_id = ObjectId(id)

    if request.method == "PUT":
        updated_data = request.json
        result = books_collection.update_one(
            {"_id": item_id},
            {"$set": updated_data}
        )

        if result.modified_count > 0:
            return jsonify({"message": "Item updated successfully"}), 200
        else:
            return jsonify({"message": "No changes made or item not found"}), 404

    itm = books_collection.find_one({"_id": item_id})
    if not itm:
        return jsonify({"error": "Book not found"}), 404

    itm["_id"] = str(itm["_id"])  # convert before returning
    return jsonify(itm)

# Delete a book by Id
@app.route('/books/<id>/delete', methods=["DELETE"])
def delete_book(id):
    
    if not ObjectId.is_valid(id):
        return jsonify({"error": "Invalid book ID"}), 400
    
    item_id = ObjectId(id)

    if request.method == "DELETE":
        try:
            del_res = books_collection.delete_one({"_id": item_id})
            print(f'[DEBUG]: Delete Result: \n{del_res}')
            return jsonify({"msg":"Record Deleted Successfyll!"})
        except Exception as e:
            print(f'[DEBUG]: Error while Delete : \n{e}')
            res = f"Error while deleting record {e}"
            return jsonify({"msg":res})
        
    itm = books_collection.find_one({"_id": item_id})
    if not itm:
        return jsonify({"error": "Book not found"}), 404

    itm["_id"] = str(itm["_id"])  # convert before returning
    return jsonify(itm)


if __name__ == "__main__":
    app.run(debug=debug_mode)