from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

tipo_medicion = {'sensor':'DHT11', 'variable':'Humedad', 'unidades': '%Agua'}

mediciones = [
    {'Fecha': '2019-06-14 11:52:43', **tipo_medicion, 'valor': 0.11},
    {'Fecha': '2019-07-17 16:34:01', **tipo_medicion, 'valor': 0.52},
    {'Fecha': '2019-07-25 20:25:10', **tipo_medicion, 'valor': 0.78},
    {'Fecha': '2019-08-22 20:46:55', **tipo_medicion, 'valor': 0.24},
    {'Fecha': '2019-08-23 10:42:10', **tipo_medicion, 'valor': 0.25},
    {'Fecha': '2019-08-23 07:00:36', **tipo_medicion, 'valor': 0.12},
    {'Fecha': '2019-08-24 02:11:28', **tipo_medicion, 'valor': 0.77}
]

@app.route('/mediciones', methods=['POST'])
def postOne():
    ahora = datetime.now()
    yson = request.json
    yson['fecha'] = datetime.strftime(ahora, '%Y-%m-%d %H:%M:%S')
    mediciones.append({**yson, **tipo_medicion})
    return jsonify(mediciones)
    
@app.route('/')
def get():
    return jsonify(tipo_medicion)

@app.route('/mediciones', methods = ['GET'])
def getAll():
    return jsonify(mediciones)

@app.route('/mediciones/media', methods = ['GET'])
def getMedia():
    media = 0
    for registros in mediciones:
        media += registros['valor']
    return jsonify(media/int(len(mediciones))) 


@app.route('/mediciones/<string:fecha>', methods=['DELETE'])
def deleteOne(fecha):
    x=False
    for registros in mediciones:
        if(fecha in registros['fecha']):
            x = True
            mediciones.remove(registros)
    return 'Eliminado' if x else 'No Encontrado'

@app.route('/mediciones/<string:fecha>', methods=['PUT'])
def putOne(fecha):
    body = request.json
    x = False
    for registros in mediciones:
        if(fecha in registros['fecha']):
            x = True
            registros['valor'] = body['valor']
    return 'Modificado' if x else 'No Encontrado'



app.run(port = 5000, debug = True)