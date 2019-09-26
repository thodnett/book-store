import os
from flask import Flask,  render_template, redirect, request, url_for, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId



app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'book_store'
app.config["MONGO_URI"] = 'mongodb+srv://thodnett:Pass1234@myfirstcluster-2pyxt.mongodb.net/book_store?retryWrites=true&w=majority'

mongo = PyMongo(app)

@app.route('/')
@app.route('/index')
def index():
    if 'username' in session:
        username = session['username']
        return render_template('index.html')
       
    return render_template('index.html')
    
@app.route('/login', methods=['POST', 'GET'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})

    if login_user:
            session['username'] = request.form['username']
            return redirect(url_for('get_books'))

    return 'Invalid username'
    
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})
        

        if existing_user is None:
            users.insert({'name' : request.form['username']})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        
        return 'That username already exists!'

    return render_template('register.html')
    
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))
    
    
@app.route('/get_books')
def get_books():
    return render_template("books.html", books=mongo.db.books.find())
        
@app.route('/add_book')
def add_book():
    if 'username' in session:
        return render_template("addbook.html",  categories=mongo.db.categories.find())
    
@app.route('/insert_book', methods=['POST'])
def insert_book():
    if 'username' in session:
        books = mongo.db.books
        books.insert_one(request.form.to_dict())
        return redirect(url_for('get_books'))
     
@app.route('/edit_book/<book_id>')
def edit_book(book_id):
    if 'username' in session:
        the_book =  mongo.db.books.find_one({"_id": ObjectId(book_id)})
        all_categories =  mongo.db.categories.find()
        return render_template('editbook.html', book=the_book, categories=all_categories)

@app.route('/update_book/<book_id>', methods=['POST'])
def update_book(book_id):
    if 'username' in session:
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
    if 'username' in session:
        mongo.db.books.remove({'_id': ObjectId(book_id)})
        return redirect(url_for('get_books'))
    
@app.route('/get_categories')
def get_categories():
    if 'username' in session:
        return render_template('categories.html', 
        categories=mongo.db.categories.find())
    
@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    if 'user' in session:
        return render_template('editcategory.html', 
        category=mongo.db.categories.find_one({'_id': ObjectId(category_id)}))
    
@app.route('/update_category/<category_id>', methods=['POST'])
def update_category(category_id):
    if 'user' in session:
            mongo.db.categories.update(
                {'_id': ObjectId(category_id)},
                {'type': request.form.get('type')})
            return redirect(url_for('get_categories'))
    
@app.route('/delete_category/<category_id>')
def delete_category(category_id):
    if 'user' in session:
        mongo.db.categories.remove({'_id': ObjectId(category_id)})
        return redirect(url_for('get_categories'))
    
@app.route('/insert_category', methods=['POST'])
def insert_category():
    if 'user' in session:
        categories = mongo.db.categories
        category_doc ={'type': request.form.get('type')}
        categories.insert_one(category_doc)
        return redirect(url_for('get_categories'))
    
    
@app.route('/add_category')
def add_category():
    if 'user' in session:
        return render_template('addcategory.html')
    
@app.route('/find_book/<type>')
def find_book(type):
    if 'user' in session:
        books=mongo.db.books.find({'category_name': type})
        return render_template('findbook.html', books=books)
    

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)