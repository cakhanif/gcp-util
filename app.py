from flask import Flask

from src.api import SecretManager, Instances
from src.cloudrun import add_domain_mapping

app = Flask(__name__)

@app.route('/secret/create_update', methods=['POST'])
def create_update_secret():
    json_data = SecretManager.create_update().get_json()
    return json_data

@app.route('/secret/view', methods=['GET'])
def view_secret():
    json_data = SecretManager.view().get_json()
    return json_data

@app.route('/instances/view', methods=['GET'])
def view_instances():
    json_data = Instances.view().get_json()
    return json_data

@app.route('/instances/get_machine_types', methods=['GET'])
def get_machine_types():
    json_data = Instances.get_machine_types().get_json()
    return json_data

@app.route('/instances/list', methods=['GET'])
def list_instances():
    json_data = Instances.list().get_json()
    return json_data

@app.route('/run/add_domain_mapping', methods=['POST'])
def add_cloudrun_domain_mapping():
    json_data = add_domain_mapping().get_json()
    return json_data

if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')