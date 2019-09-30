import requests, ast, json
from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, World!"

@app.route("/history", methods = ["GET"])
def history():
    image_name = request.args.get('name', '')
    image_tag = request.args.get('tag', '')
    return getImageHistory(image_name, image_tag)

def getImageHistory(image_name, image_tag):
    url = 'http://registry:5000/v2/{}/manifests/{}'.format(image_name, image_tag)
    headers = {'Content-type': 'application/json; charset=UTF-8'}
    response = requests.get(url)
    json_data = response.json() if response and response.status_code == 200 else None
    my_list = []
    for it in json_data['history']:
      for it1 in it.values():
        it2 = json.loads(it1)
        try:
          my_list.append(' '.join(it2['container_config']['Cmd']))
        except ValueError:
          print "Not a dict: {}".format(it2)
    return_text = '</br>'.join(my_list)
    return render_template_string(return_text)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=80)
