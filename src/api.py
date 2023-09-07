from flask import jsonify, request
import json
from google.cloud import secretmanager, compute_v1 as compute

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
    

class Instances:
    def list():

        # get the request data
        request_data = request.get_json()

        # Extract the project ID from the request data
        project_id = request_data['project_id']

        # Create a client object to interact with the Compute Engine API
        client = compute.InstancesClient()

        # Retrieve a list of all regions and zones
        list = client.aggregated_list(project=project_id)
        # Initialize an empty list to store all compute engine instances
        all_compute_engines = []

        # # Loop over all regions and zones to retrieve the compute engine instances
        # for region in list['items']:
        #     for zone in region['zones']:
        #         zone_name = zone.split('/')[-1]
        #         instances = client.instances().list(project=project_id, zone=zone_name)
        #         if 'items' in instances:
        #             all_compute_engines.extend(instances['items'])

        # response = {
        #     'compute_engines': all_compute_engines
        # }
        response = list

        # Return the list of all compute engines as a JSON response
        return jsonify(response)
    
    def view():
        """
        Retrieves the details of a virtual machine from Google Compute Engine.

        Request Body:
            project_id (str): The ID of the project in which the virtual machine exists.
            zone (str): The zone in which the virtual machine exists.
            instance_id (str): The ID of the virtual machine to retrieve.

        Returns:
            A JSON response containing the details of the virtual machine.
        """

        # Get the request data
        request_data = request.get_json()

        # Extract the project ID, zone, and instance ID from the request data
        project_id = request_data['project_id']
        zone = request_data['zone']
        instance_id = request_data['instance_id']

        # Create the Compute Engine client
        client = compute.InstancesClient()

        # Build the instance name
        name = f"projects/{project_id}/zones/{zone}/instances/{instance_id}"

        # Retrieve the instance
        response = client.get(project=project_id, zone=zone, instance=instance_id)
        instance = response.name

        # Return a JSON response containing the details of the virtual machine
        response = {
            'instance': instance
        }
        return jsonify(response)
    
    def get_machine_types():
        """
        Retrieves the available machine types from Google Compute Engine.

        Request Body:
            project_id (str): The ID of the project in which to retrieve the machine types.
            zone (str): The zone in which to retrieve the machine types.

        Returns:
            A JSON response containing the available machine types.
        """

        # Get the request data
        request_data = request.get_json()

        # Extract the project ID and zone from the request data
        project_id = request_data['project_id']
        zone = request_data['zone']

        # Create the Compute Engine client
        client = compute.MachineTypesClient()

        # Retrieve the machine types
        response = client.list(project=project_id, zone=zone)
        machine_types = [machine_type.name for machine_type in response]

        # Return a JSON response containing the available machine types
        response = {
            'machine_types': machine_types
        }
        return jsonify(response)

    def create():
        """
        Creates a new virtual machine in Google Compute Engine.

        Request Body:
            project_id (str): The ID of the project in which to create the virtual machine.
            zone (str): The zone in which to create the virtual machine.
            instance_id (str): The ID to assign to the virtual machine.
            machine_type (str): The machine type to assign to the virtual machine.
            source_image (str): The source image to use for the virtual machine.

        Returns:
            A JSON response containing a message indicating whether the virtual machine was created successfully.
        """

        # Get the request data
        request_data = request.get_json()

        # Extract the project ID, zone, instance ID, machine type, and source image from the request data
        project_id = request_data['project_id']
        zone = request_data['zone']
        instance_id = request_data['instance_id']
        machine_type = request_data['machine_type']
        source_image = request_data['source_image']

        # Create the Compute Engine client
        client = compute.ComputeEngineClient()

        # Build the instance name
        name = f"projects/{project_id}/zones/{zone}/instances/{instance_id}"

        # Build the instance config
        machine_type = f"projects/{project_id}/zones/{zone}/machineTypes/{machine_type}"
        source_image = f"projects/{project_id}/global/images/{source_image}"
        config = compute.Instance(name=name, machine_type=machine_type, source_image=source_image)

        # Create the instance
        operation = client.insert_instance(request={"project": project_id, "zone": zone, "instance_resource": config})
        operation.wait()

        # Return a JSON response indicating whether the virtual machine was created successfully
        response = {
            'message': f"Instance '{instance_id}' created in project '{project_id}'"
        }
        return jsonify(response)