# Book Management API

A simple RESTful Book Management API built with **Flask** and **MongoDB**.  
This API allows you to create, read, update, and delete books from a MongoDB database.

---

## Features

- Connects to MongoDB using `pymongo`
- Environment variable support using `.env`
- CRUD operations for Books
- ObjectId validation
- JSON responses
- Debug mode configurable via environment variable

---

## Tech Stack

- Python
- Flask
- MongoDB
- PyMongo
- python-dotenv

---

## Project Structure

```

.
├── wsgi.py
├── requirements.txt
├── .env
├── .gitignore

```

---

## Environment Variables

Create a .env file in the root directory:

```

DATABASE_URL=mongodb://localhost:27017/
SECRET_KEY=your_secret_key_here
DEBUG_MODE=True

```

Environment Variables Explained

```
DATABASE_URL = MongoDB connection string
SECRET_KEY = Flask secret key
DEBUG_MODE = True/False for debug mode
```
---
## Installation

### 1️ Clone the repository

```

git clone <your-repo-url>
cd <your-project-folder>

```

### 2️ Create Virtual Environment

```

python -m venv venv

```

Activate it:

**Windows**
```

venv\Scripts\activate

```

**Mac/Linux**
```

source venv/bin/activate

```

### 3️ Install Dependencies

```

pip install -r requirements.txt

```

---

## Run the Application

```

python wsgi.py

```

Server will start at:

```

[http://127.0.0.1:5000/](http://127.0.0.1:5000/)

````

---

# API Endpoints

---

## 1 Health Check

### `GET /`

**Response**
```json
{
  "msg": "Book Management API is Running."
}
````

---

## 2️ List All Books

### `GET /books/list/`

Returns all books in the database.

---

## 3️ Add a Book

### `POST /books/add/`

**Request Body**

```json
{
  "title": "Atomic Habits",
  "author": "James Clear",
  "price": 499
}
```

**Response**

```json
{
  "msg": "Book added Successfully!"
}
```

---

## 4️ Get Book by ID

### `GET /books/<id>/`

Returns a single book by MongoDB ObjectId.

---

## 5️ Update Book

### `PATCH /books/<id>/update/`

**Request Body**

```json
{
  "price": 599
}
```

**Response**

```json
{
  "message": "Item updated successfully"
}
```

---

## 6️ Delete Book

### `DELETE /books/<id>/delete/`

**Response**

```json
{
  "msg": "Record Deleted Successfully!"
}
```

---

## Testing

You can test the API using:

* Postman
* Thunder Client (VS Code)
* curl

---

## Important Notes

* `.env` file should not be committed to GitHub
* MongoDB must be running locally or use a cloud connection string
* Always validate ObjectId before database operations

---

## License

* This project is open-source and free to use.
