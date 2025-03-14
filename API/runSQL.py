from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configurar la conexión a SQL Server
#API_URL = "http://3.149.244.248:3002/v1/books"
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc://sa:1234@LAPTOP-JAR0CAFN\\SQLEXPRESS/BibliotecaAPI?driver=ODBC+Driver+17+for+SQL+Server"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de la tabla libros
class Libro(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    libroname = db.Column(db.String(255), nullable=False)
    autor = db.Column(db.String(255), nullable=False)

# Crear las tablas si no existen
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    libros = Libro.query.all()
    return render_template('index.html', libros=libros)

# Obtener todos los libros (GET)
@app.route('/libros', methods=['GET'])
def getList():
    libros = Libro.query.all()
    return jsonify([{'id': l.id, 'libroname': l.libroname, 'autor': l.autor} for l in libros])

# Obtener un libro por ID (GET)
@app.route('/libros/<int:id>', methods=['GET'])
def getDetail(id):
    libro = Libro.query.get_or_404(id)
    return jsonify({'id': libro.id, 'libroname': libro.libroname, 'autor': libro.autor})

# Crear un nuevo libro (POST)
@app.route('/libros', methods=['POST'])
def createItem():
    data = request.json
    new_libro = Libro(libroname=data['libroname'], autor=data['autor'])
    db.session.add(new_libro)
    db.session.commit()
    return jsonify({'message': 'Libro agregado exitosamente'}), 201

# Actualizar un libro (PUT)
@app.route('/libros/<int:id>', methods=['PUT'])
def updateItem(id):
    libro = Libro.query.get_or_404(id)
    data = request.json
    libro.libroname = data['libroname']
    libro.autor = data['autor']
    db.session.commit()
    return jsonify({'message': 'Libro actualizado exitosamente'})

# Ruta para editar un libro desde la web
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    libro = Libro.query.get_or_404(id)
    if request.method == 'POST':
        libro.libroname = request.form['libroname']
        libro.autor = request.form['autor']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', libro=libro)

# Eliminar un libro (DELETE)
@app.route('/libros/<int:id>', methods=['DELETE'])
def deleteItem(id):
    libro = Libro.query.get_or_404(id)
    db.session.delete(libro)
    db.session.commit()
    return jsonify({'message': 'Libro eliminado exitosamente'})

# Ruta para agregar un libro desde la web
@app.route('/add', methods=['POST'])
def add_item():
    libroname = request.form['libroname']
    autor = request.form['autor']
    new_libro = Libro(libroname=libroname, autor=autor)
    db.session.add(new_libro)
    db.session.commit()
    return redirect(url_for('index'))

# Ruta para eliminar un libro desde la web
@app.route('/delete/<int:id>')
def delete(id):
    libro = Libro.query.get_or_404(id)
    db.session.delete(libro)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
