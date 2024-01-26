from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(_name_)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)

    def _repr_(self):
        return f'<Book {self.title}>'

@app.before_first_request
def create_tables():
    db.create_all()

# Add more routes here
@app.route('/books')
def books():
    all_books = Book.query.all()
    return render_template('books.html', books=all_books)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        new_book = Book(
            title=request.form['title'],
            author=request.form['author'],
            publication_year=request.form['publication_year']
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('books'))
    return render_template('add_book.html')

if _name_ == '_main_':
    app.run(debug=True)