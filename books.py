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
        
app.run()

