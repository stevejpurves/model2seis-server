import sys
import os
sys.path.append(os.path.abspath('./src'))
from flask import Flask, request, send_from_directory, jsonify
import json
import numpy as np
app = Flask(__name__, static_url_path='')


@app.route('/api/model/<id>')
def get_model(id):
  filename = 'model' + str(id) + '.png';
  return app.send_static_file('data/' + filename)

@app.route('/api/forward', methods=['POST'])
def get_forward_model():
  seismic= model2seismic()
  return jsonify({"seismic": list(seismic)})
  
@app.route('/api/inverse')
def get_inverse_model():
  model = seismic2model()
  return jsonify(model)

@app.route('/api/heartbeat')
def pong():
  return jsonify({"ReturnCode": 200})

@app.route('/')
def root():
  return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_proxy(path):
  # send_static_file will guess the correct MIME type
  return app.send_static_file(path)

if __name__ == "__main__":
    app.run(debug=True)
