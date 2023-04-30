from flask import Flask

from api import SecretManager

app = Flask(__name__)

@app.route('/secret/create_update', methods=['POST'])
def create_update_secret():
    json_data = SecretManager.create_update().get_json()
    return json_data

@app.route('/secret/view', methods=['GET'])
def view_secret():
    json_data = SecretManager.view().get_json()
    return json_data



if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')