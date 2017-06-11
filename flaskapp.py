import sys
import os
sys.path.append(os.path.abspath('./src'))
from flask import Flask, request, send_from_directory, jsonify
import json
import string,time,hashlib
import numpy as np
import urllib, cStringIO
from tempfile import NamedTemporaryFile
from src import sketch2model

app = Flask(__name__, static_url_path='')


@app.route('/api/model/<id>')
def get_model(id):
  filename = str(id) + '.png';
  return app.send_static_file('tmp/' + filename)

@app.route('/api/forward', methods=['POST'])
def get_forward_model():
  #tempFileObj = NamedTemporaryFile(mode='w+b',suffix='jpg')
  body = request.get_json(force=True)
  [_,data]=body['dataUrl'].split(',')
  #binary_data = a2b_base64(data['dataUrl'])
  binary_data = data.decode('base64')
  hash = hashlib.sha1()
  hash.update(str(time.time()))
  name=hash.hexdigest()[:10]
  fd = open('./tmp/'+name+'.png','wb')
  fd.write(binary_data)
  fd.close
  r = sketch2model.call_sketch2model(url="http://ec2-35-158-38-106.eu-central-1.compute.amazonaws.com/tmp/"+name)
  #tempFileObj = cStringIO.StringIO(urllib.urlopen(r['url']).read())  
  #tempFileObj.seek(0,0)
  #response = send_file(tempFileObj, attachment_filename='myfile.png')
  return jsonify({ "modelUrl": '/api/model/'+name, "seismicUrl": '/api/model/'+name })

@app.route('/api/forward-model_only')
def get_forward_from_model_only():
  body = request.get_json(force=True)
  modelUrl = body['modelUrl']
  # download to temp
  # run model2sketch
  # return { seismicUrl }

@app.route('/api/inverse')
def get_inverse_model():
  model = seismic2model()
  return jsonify(model)

@app.route('/api/heartbeat')
def pong():
  return jsonify({"ok": True})


@app.route('/')
def root():
  return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_proxy(path):
  # send_static_file will guess the correct MIME type
  return app.send_static_file(path)

if __name__ == "__main__":
    app.run(debug=True)
