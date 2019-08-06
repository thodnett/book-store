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

@app.route('/update_book/<book_id>', methods=['POST'])
def update_book(book_id):
    books = mongo.db.books
    books.update( {'_id': ObjectId(book_id)},
    {
        'book_name':request.form.get('book_name'),
        'category_name':request.form.get('category_name'),
        'book_author':request.form.get('book_author'),
        'book_descrip':request.form.get('book_descrip'),
        'book_review':request.form.get('book_review'),
        'cover_link':request.form.get('cover_link'),
        'purch_link':request.form.get('purch_link')
    })
    return redirect(url_for('get_books'))

@app.route('/delete_book/<book_id>')
def delete_book(book_id):
    mongo.db.books.remove({'_id': ObjectId(book_id)})
    return redirect(url_for('get_books'))
    
@app.route('/get_categories')
def get_categories():
    return render_template('categories.html', 
    categories=mongo.db.categories.find())
    
@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    return render_template('editcategory.html', 
    category=mongo.db.categories.find_one({'_id': ObjectId(category_id)}))
    
@app.route('/update_category/<category_id>', methods=['POST'])
def update_category(category_id):
    mongo.db.categories.update(
        {'_id': ObjectId(category_id)},
        {'category_name': request.form.get('category_name')})
    return redirect(url_for('get_categories'))
    
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)