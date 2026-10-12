#!/usr/bin/env python3
"""Manual OAuth flow - output auth URL, read back auth code."""

import json, os, sys
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
        "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob"]
    }
}

flow = InstalledAppFlow.from_client_config(CLIENT_CONFIG, SCOPES)

# Use OOB (out-of-band) flow - Google gives a code you paste back
auth_url, _ = flow.authorization_url(
    access_type='offline',
    include_granted_scopes='true',
    prompt='consent'
)

print("=" * 60)
print("AUTH_URL:" + auth_url)
print("=" * 60)
print()
print("Visit the URL above in your browser.")
print("After authorizing, Google will show you a code.")
print("Paste that code below and press Enter.")
print()
sys.stdout.flush()

# Read code from stdin
auth_code = sys.stdin.readline().strip()
if not auth_code:
    print("No code provided.")
    sys.exit(1)

print(f"Exchanging code: {auth_code[:20]}...")
creds = flow.fetch_token(code=auth_code)

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
    json.dump(token_data, f)

print("TOKEN_SAVED:/tmp/gsheets-token.json")
print(f"Token expires: {creds.expiry}")
