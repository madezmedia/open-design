#!/usr/bin/env python3
"""OAuth flow — prints auth URL, starts local server on fixed port."""

import json, os
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
]

CLIENT_CONFIG = {
    "installed": {
        "client_id": "32555940559.apps.googleusercontent.com",
        "project_id": "project-82b1c6fe-ab8a-42fb-949",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "redirect_uris": ["http://localhost"]
    }
}

if __name__ == '__main__':
    flow = InstalledAppFlow.from_client_config(CLIENT_CONFIG, SCOPES)
    flow.redirect_uri = 'http://localhost:8080/'

    creds = flow.run_local_server(
        host='localhost',
        port=8080,
        open_browser=False,
        authorization_prompt_message=""
    )

    with open('/tmp/gsheets-token.json', 'w') as f:
        f.write(creds.to_json())

    print("TOKEN_SAVED:/tmp/gsheets-token.json")
