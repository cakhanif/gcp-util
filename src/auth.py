# import os
# import google.auth
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request

# class Auth:
#     def get_auth_token(scopes, credentials_file, token_file):
#         """
#         Authenticate with Google API client and get access token
#         """
#         # Get credentials from file or environment variable
#         credentials = Credentials.from_authorized_user_file(credentials_file, scopes)

#         # If credentials are expired or not found, refresh them
#         if not credentials or not credentials.valid:
#             if credentials and credentials.expired and credentials.refresh_token:
#                 credentials.refresh(Request())
#             else:
#                 flow = google.auth.default(scopes)
#                 credentials = flow.run_local_server(port=0)

#             # Save the credentials to a file for future use
#             with open('path/to/credentials.json', 'w') as credentials_file:
#                 credentials_file.write(credentials.to_json())

#         # Return the access token
#         return credentials.token

#     # def authenticate(scopes, credentials_file, token_file):
#     #     # # Set up Google Cloud Run credentials
#     #     # credentials = google.auth.default() #can use default credential or basic credential
#     #     # creds = Credentials.from_authorized_user_info(info=credentials)
        
#     #     # return creds    

#     #     # Load the access token and refresh token from the JSON file, if available.
#     #     try:
#     #         creds = Credentials.from_authorized_user_file(token_file, scopes)
#     #     except FileNotFoundError:
#     #         creds = None
        
#     #     # If the credentials are not valid, prompt the user to authorize the app.
#     #     if not creds or not creds.valid:
#     #         flow = InstalledAppFlow.from_client_secrets_file(credentials_file, scopes)
#     #         creds = flow.run_local_server(port=0)
            
#     #         # Save the access token and refresh token for future use.
#     #         with open(token_file, 'w') as f:
#     #             f.write(creds.to_json())
        
#     #     return creds



