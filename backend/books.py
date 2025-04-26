from creds import Creds
from sql import create_conn
import flask
from flask import jsonify, request


app = flask.Flask(__name__)
app.config['DEBUG'] = True

db = create_conn()


@app.route('/api/books/all', methods = ['GET'])
def get_all():
    try:
        cursor = db.cursor(dictionary=True)  # Ensure cursor is created inside the function
        cursor.execute("SELECT * FROM books")
        books = cursor.fetchall()
        cursor.close()  # Close cursor after fetching data
        return jsonify(books)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
@app.route('/api/books', methods = ['POST'])
def create_new():
    try:
        data = request.json
        title = data.get('title')
        author = data.get('author')
        genre = data.get('genre')
        status = data.get('status', 'available')  

        if not title or not author or not genre:
            return jsonify({"error": "Title, author, and genre are required"}), 400

        cursor = db.cursor()
        cursor.execute("INSERT INTO books (title, author, genre, status) VALUES (%s, %s, %s, %s)", (title, author, genre, status))
        db.commit()
        cursor.close()
        return jsonify({"message": "Book created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/books/<int:id>', methods=['PUT'])
def update_book(id):
    try:
        data = request.json
        title = data.get('title')
        author = data.get('author')
        genre = data.get('genre')
        status = data.get('status')

        if not any([title, author, genre, status]):
            return jsonify({"error": "At least one field is required for update"}), 400

        cursor = db.cursor()
        query = "UPDATE books SET "
        updates = []
        values = []

        if title:
            updates.append("title = %s")
            values.append(title)
        if author:
            updates.append("author = %s")
            values.append(author)
        if genre:
            updates.append("genre = %s")
            values.append(genre)
        if status:
            updates.append("status = %s")
            values.append(status)

        query += ", ".join(updates) + " WHERE id = %s"
        values.append(id)

        cursor.execute(query, values)
        db.commit()
        cursor.close()

        if cursor.rowcount == 0:
            return jsonify({"error": "Book not found"}), 404

        return jsonify({"message": "Book updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    try:
        cursor = db.cursor()
        cursor.execute("DELETE FROM books WHERE id = %s", (id,))
        db.commit()
        cursor.close()

        if cursor.rowcount == 0:
            return jsonify({"error": "Book not found"}), 404

        return jsonify({"message": "Book deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

app.run()

