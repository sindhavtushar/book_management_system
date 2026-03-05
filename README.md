# Book Management API

A simple app serving HTML views and REST API endpoints, built with **Flask** and **MongoDB**.  
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
│   .env
│   .gitignore
│   README.md
│   requirements.txt
│   wsgi.py
│
├───app
│   │   __init__.py
│   │
│   ├───api
│   │   │   books.py
│   │
│   ├───templates
│   │       base.html
│   │       book-dashboard.html
│   │       book-detail.html
│   │       index.html
│   │
│   ├───views
│   │   │   books.py

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

git clone <repo-url>
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

### `GET /api/`

**Response**
```json
{
  "msg": "Book Management API is Running."
}
````

---

## 2️ List All Books

### `GET /api/books/list/`

Returns all books in the database.

---

## 3️ Add a Book

### `POST /api/books/add/`

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

### `GET /api/books/<id>/`

Returns a single book by MongoDB ObjectId.

---

## 5️ Update Book

### `PATCH /api/books/<id>/update/`

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

### `DELETE /api/books/<id>/delete/`

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

# UI Routes (Template Views)

These routes render HTML pages using Flask templates. Defined in `app/views/books.py`, they use templates from `app/templates/`.

| Route | Template | Description |
|-------|---------|-------------|
| `/` | `index.html` | Home page |
| `/books/dashboard/` | `book-dashboard.html` | Books dashboard page |
| `/books/<id>/` | `book-detail.html` | Book detail page (uses `bookId` parameter) |

### Example Usage

- Open a browser and go to `/` to view the home page.
- Navigate to `/books/dashboard/` to view the dashboard UI.
- Navigate to `/books/<id>/` to view details of a specific book.

### Data Fetching

- The templates fetch data from the API endpoints using JavaScript (fetch):
- book-dashboard.html → fetches /api/books/list/ to display all books.
- book-detail.html → fetches /api/books/id/ to show details for a single book.

- This makes the UI dynamic while keeping the API reusable for external clients.

## Important Notes

* `.env` file should not be committed to GitHub
* MongoDB must be running locally or use a cloud connection string
* Always validate ObjectId before database operations

---

## License

* This project is open-source and free to use.
