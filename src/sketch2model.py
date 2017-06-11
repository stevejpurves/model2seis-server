import requests
from tempfile import NamedTemporaryFile
from shutil import copyfileobj
from os import remove

def call_sketch2model(url):
  contrast = "0.5"
  closing = "3"
  cmap = "Pstel2"
  payload = {
  "url": url,
  "contrast": contrast,
  "closing": closing,
  "cmap": cmap}

  headers = {"Accept": "application/json"}

  r = requests.get("http://www.sketch2model.com/api",
  headers=headers,
  params=payload)
  return r.json()

def serve_model():
  tempFileObj = NamedTemporaryFile(mode='w+b',suffix='jpg')
  pilImage = open('/tmp/myfile.jpg','rb')
  copyfileobj(pilImage,tempFileObj)
  pilImage.close()
  remove('/tmp/myfile.jpg')
  tempFileObj.seek(0,0)

if __name__ == "__main__":
  print call_sketch2model()

