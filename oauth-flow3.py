#!/usr/bin/env python3
"""OAuth flow using local server. Writes auth URL to file, waits for callback."""

import json, os, sys, socket, threading, time, http.server, urllib.parse
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

# Let it pick a random port
flow = InstalledAppFlow.from_client_config(CLIENT_CONFIG, SCOPES)

# Don't set redirect_uri - let it use the default localhost with random port
creds = flow.run_local_server(
    open_browser=False,
    authorization_prompt_message=""
)

# Save token
token_data = {
    'token': creds.token,
    'refresh_token': creds.refresh_token,
    'token_uri': creds.token_uri,
    'client_id': creds.client_id,
    'client_secret': creds.client_secret,
    'scopes': creds.scopes,
    'expiry': creds.expiry.isoformat() if creds.expiry else None
}

with open('/tmp/gsheets-token.json', 'w') as f:
    f.write(json.dumps(token_data))

print("TOKEN_SAVED:/tmp/gsheets-token.json", flush=True)
