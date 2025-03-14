import requests
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

API_URL = "http://3.149.244.248:3002/v1/books"

@app.route('/')
def index():
    response = requests.get(API_URL)

    if response.status_code != 200:
        return f"Error al obtener datos de la API. Código: {response.status_code}", 500
    
    try:
        libros = response.json()
    except ValueError:
        return f"Error: No se pudo convertir la respuesta en JSON. Respuesta recibida: {response.text}", 500

    if isinstance(libros, dict) and "data" in libros:
        libros = libros["data"]

    if not isinstance(libros, list):
        return f"Error: La API devolvió datos en un formato inesperado ({type(libros)}). Contenido: {libros}", 500

    for libro in libros:
        if isinstance(libro, dict) and "idlibro" in libro:
            libro["id"] = libro.pop("idlibro", None)

    return render_template('index.html', libros=libros)

@app.route('/libros', methods=['GET'])
def getList():
    response = requests.get(API_URL)
    return jsonify(response.json())

@app.route('/libros/<int:id>', methods=['GET'])
def getDetail(id):
    response = requests.get(f"{API_URL}/{id}")
    return jsonify(response.json())

@app.route('/libros', methods=['POST'])
def createItem():
    data = request.json
    response = requests.post(API_URL, json=data)
    return jsonify(response.json()), response.status_code

@app.route('/libros/<int:id>', methods=['PUT'])
def updateItem(id):
    data = request.json
    response = requests.put(f"{API_URL}/{id}", json=data)
    return jsonify(response.json()), response.status_code

@app.route('/libros/<int:id>', methods=['DELETE'])
def deleteItem(id):
    response = requests.delete(f"{API_URL}/{id}")
    return jsonify(response.json()), response.status_code

@app.route('/add', methods=['POST'])
def add_item():
    libroname = request.form['libroname']
    autor = request.form['autor']
    response = requests.post(API_URL, json={'libroname': libroname, 'autor': autor})
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        libroname = request.form['libroname']
        autor = request.form['autor']
        response = requests.put(f"{API_URL}/{id}", json={'libroname': libroname, 'autor': autor})
        return redirect(url_for('index'))
    else:
        response = requests.get(f"{API_URL}/{id}")
        libro = response.json() if response.status_code == 200 else None
        return render_template('edit.html', libro=libro)

@app.route('/delete/<int:id>')
def delete(id):
    requests.delete(f"{API_URL}/{id}")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
