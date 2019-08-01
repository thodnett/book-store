import os
from flask import Flask,  render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'book_store'
app.config["MONGO_URI"] = 'mongodb+srv://thodnett:Pass1234@myfirstcluster-2pyxt.mongodb.net/book_store?retryWrites=true&w=majority'

mongo = PyMongo(app)



@app.route('/')
@app.route('/get_books')
def get_books():
    return render_template("books.html", books=mongo.db.books.find())
    
@app.route('/add_book')
def add_book():
    return render_template("addbook.html",  categories=mongo.db.categories.find())
    
@app.route('/insert_book', methods=['POST'])
def insert_book():
    books = mongo.db.books
    books.insert_one(request.form.to_dict())
    return redirect(url_for('get_books'))
    
@app.route('/edit_book/<book_id>')
def edit_book(book_id):
    the_book =  mongo.db.books.find_one({"_id": ObjectId(book_id)})
    all_categories =  mongo.db.categories.find()
    return render_template('editbook.html', book=the_book, categories=all_categories)

   
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)