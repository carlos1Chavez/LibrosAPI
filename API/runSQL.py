from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#API_URL = "http://3.149.244.248:3002/v1/books"
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc://sa:1234@LAPTOP-JAR0CAFN\\SQLEXPRESS/BibliotecaAPI?driver=ODBC+Driver+17+for+SQL+Server"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Libro(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    libroname = db.Column(db.String(255), nullable=False)
    autor = db.Column(db.String(255), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    libros = Libro.query.all()
    return render_template('index.html', libros=libros)

@app.route('/libros', methods=['GET'])
def getList():
    libros = Libro.query.all()
    return jsonify([{'id': l.id, 'libroname': l.libroname, 'autor': l.autor} for l in libros])

@app.route('/libros/<int:id>', methods=['GET'])
def getDetail(id):
    libro = Libro.query.get_or_404(id)
    return jsonify({'id': libro.id, 'libroname': libro.libroname, 'autor': libro.autor})

@app.route('/libros', methods=['POST'])
def createItem():
    data = request.json
    new_libro = Libro(libroname=data['libroname'], autor=data['autor'])
    db.session.add(new_libro)
    db.session.commit()
    return jsonify({'message': 'Libro agregado exitosamente'}), 201

@app.route('/libros/<int:id>', methods=['PUT'])
def updateItem(id):
    libro = Libro.query.get_or_404(id)
    data = request.json
    libro.libroname = data['libroname']
    libro.autor = data['autor']
    db.session.commit()
    return jsonify({'message': 'Libro actualizado exitosamente'})

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    libro = Libro.query.get_or_404(id)
    if request.method == 'POST':
        libro.libroname = request.form['libroname']
        libro.autor = request.form['autor']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', libro=libro)

@app.route('/libros/<int:id>', methods=['DELETE'])
def deleteItem(id):
    libro = Libro.query.get_or_404(id)
    db.session.delete(libro)
    db.session.commit()
    return jsonify({'message': 'Libro eliminado exitosamente'})

@app.route('/add', methods=['POST'])
def add_item():
    libroname = request.form['libroname']
    autor = request.form['autor']
    new_libro = Libro(libroname=libroname, autor=autor)
    db.session.add(new_libro)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    libro = Libro.query.get_or_404(id)
    db.session.delete(libro)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
