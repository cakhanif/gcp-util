from flask import jsonify, request
from google.cloud import secretmanager

class SecretManager:
    def view():
        """
        Retrieves the value of a secret from Google Secret Manager.

        Request Body:
            project_id (str): The ID of the project in which the secret exists.
            secret_id (str): The ID of the secret to retrieve.

        Returns:
            A JSON response containing the value of the secret.
        """

        # Get the request data
        request_data = request.get_json()

        # Extract the project ID and secret ID from the request data
        project_id = request_data['project_id']
        secret_id = request_data['secret_id']
        secret_version = request_data['secret_version']

        # Create the Secret Manager client
        client = secretmanager.SecretManagerServiceClient()

        # Build the secret name
        name = f"projects/{project_id}/secrets/{secret_id}/versions/{secret_version}"

        # Retrieve the secret
        response = client.access_secret_version(name=name)
        secret_data = response.payload.data.decode('utf-8')

        # Return a JSON response containing the value of the secret
        response = {
            'secret_data': secret_data
        }
        return jsonify(response)
    
    def create_update():
        """
        Creates a new secret or updates an existing one in Google Secret Manager.
        If the secret already exists, its value will be updated with the new data.

        Request Body:
            project_id (str): The ID of the project in which to create the secret.
            secret_id (str): The ID of the secret to create or update.
            secret_data (str): The data to store in the secret.

        Returns:
            A JSON response containing a message indicating whether the secret was created or updated successfully.
        """

        # Get the request data
        request_data = request.get_json()

        # Extract the project ID, secret ID, and secret data from the request data
        project_id = request_data['project_id']
        secret_id = request_data['secret_id']
        secret_data = request_data['secret_data']

        # Create the Secret Manager client
        client = secretmanager.SecretManagerServiceClient()

        # Build the secret name
        name = f"projects/{project_id}/secrets/{secret_id}"

        # Check if the secret already exists
        try:
            client.get_secret(name=name)
            # If the secret exists, update its value
            payload = secretmanager.SecretPayload(data=secret_data.encode('utf-8'))
            client.update_secret(name=name, secret=secretmanager.Secret(payload=payload))
            message = f"Secret '{secret_id}' updated in project '{project_id}'"
        except:
            # If the secret doesn't exist, create it
            parent = f"projects/{project_id}"
            payload = secretmanager.SecretPayload(data=secret_data.encode('utf-8'))
            secret = secretmanager.Secret(payload=payload)
            client.create_secret(parent=parent, secret_id=secret_id, secret=secret)
            message = f"Secret '{secret_id}' created in project '{project_id}'"

        # Return a JSON response indicating whether the secret was created or updated successfully
        response = {
            'message': message
        }
        return jsonify(response)