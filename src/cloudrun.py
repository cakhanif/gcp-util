from flask import request

import requests
import google.auth
from google.oauth2.credentials import Credentials
from google.cloud import run

from src.auth import Auth

creds = Auth.get_auth_token(scopes, credentials_file, token_file)


# def auth_google_webmaster():
#     # Set up Google Webmaster Tools API endpoint and authorization headers
#     webmasters_api_url = 'https://www.googleapis.com/webmasters/v3/sites/{}/verification'
#     webmasters_auth_headers = {
#         'Authorization': f'Bearer {creds.token}',
#         'Content-Type': 'application/json'
#     }
    
#     # Get the domain from the request
#     domain = request.json.get('domain')
    
#     # Verify the domain with Google Webmaster Tools
#     webmasters_api_response = requests.post(
#         webmasters_api_url.format(domain),
#         headers=webmasters_auth_headers,
#         json={
#             'verificationMethod': 'DNS_TXT',
#             'dnsVerification': {
#                 'token': request.json.get('token')
#             }
#         }
#     )
    
#     # Return the verification value
#     return webmasters_api_response.json()['token']

# Set up Google Webmaster Tools API endpoint and authorization headers
webmasters_api_url = 'https://www.googleapis.com/webmasters/v3/sites/{}/verification'
webmasters_auth_headers = {
    'Authorization': f'Bearer {creds.token}',
    'Content-Type': 'application/json'
}

def add_domain_mapping():
    # Get the domain and Cloud Run service name from the request
    domain = request.json.get('domain')
    service_name = request.json.get('service_name')
    project_id = request.json_get('project_id')
    
    # Create the Cloud Run client and create the domain mapping
    client = run.RunServiceClient()
    operation = client.create_domain_mapping(
        parent=f'namespaces/{project_id}/services/{service_name}',
        domain_mapping={'name': domain}
    )
    operation.result()
    
    # Verify the domain with Google Webmaster Tools
    webmasters_api_response = requests.post(
        webmasters_api_url.format(domain),
        headers=webmasters_auth_headers,
        json={
            'verificationMethod': 'DNS_TXT',
            'dnsVerification': {
                'token': operation.metadata.annotations['x-goog-request-params'].split('=')[1]
            }
        }
    )
    
    # Return the verification value
    return webmasters_api_response.json()['token']