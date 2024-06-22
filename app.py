from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Ruta del archivo JSON
FILE_PATH = 'deportes.json'

# Función para leer los datos del archivo JSON
def read_json():
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r') as file:
            return json.load(file)
    return []

# Función para escribir los datos en el archivo JSON
def write_json(data):
    with open(FILE_PATH, 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/deporte', methods=['POST'])
def add_deporte():
    data = request.json
    nombre = data.get('nombre')
    precio = data.get('precio')

    if not nombre or not precio:
        return jsonify({'error': 'Nombre y precio son requeridos'}), 400

    deportes = read_json()
    nuevo_deporte = {'nombre': nombre, 'precio': precio}
    deportes.append(nuevo_deporte)
    write_json(deportes)

    return jsonify({'message': 'Deporte agregado correctamente'}), 201

@app.route('/deportes', methods=['GET'])
def get_deportes():
    deportes = read_json()
    return jsonify(deportes), 200

@app.route('/deporte', methods=['PUT'])
def update_deporte():
    data = request.json
    nombre = data.get('nombre')
    nuevo_precio = data.get('precio')

    if not nombre or not nuevo_precio:
        return jsonify({'error': 'Nombre y nuevo precio son requeridos'}), 400

    deportes = read_json()
    deporte_encontrado = False

    for deporte in deportes:
        if deporte['nombre'] == nombre:
            deporte['precio'] = nuevo_precio
            deporte_encontrado = True
            break

    if not deporte_encontrado:
        return jsonify({'error': 'Deporte no encontrado'}), 404

    write_json(deportes)
    return jsonify({'message': 'Precio actualizado correctamente'}), 200

@app.route('/deporte', methods=['DELETE'])
def delete_deporte():
    data = request.json
    nombre = data.get('nombre')

    if not nombre:
        return jsonify({'error': 'Nombre es requerido'}), 400

    deportes = read_json()
    deportes = [deporte for deporte in deportes if deporte['nombre'] != nombre]

    write_json(deportes)
    return jsonify({'message': 'Deporte eliminado correctamente'}), 200

if __name__ == '__main__':
    app.run(debug=True)
