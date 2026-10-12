#!/usr/bin/env python3
"""OAuth flow for Google Sheets API - outputs URL for browser auth."""

import json
import os
import socketserver
import http.server
import webbrowser
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
]

# Create flow
flow = InstalledAppFlow.from_client_config(
    {
        "installed": {
            "client_id": "32555940559.apps.googleusercontent.com",
            "project_id": "project-82b1c6fe-ab8a-42fb-949",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "redirect_uris": ["http://localhost"]
        }
    },
    SCOPES
)

# Generate authorization URL
auth_url, _ = flow.authorization_url(
    access_type='offline',
    include_granted_scopes='true',
    prompt='consent'
)

print("=" * 70)
print("  GOOGLE SHEETS API — AUTHORIZATION REQUIRED")
print("=" * 70)
print()
print("  Visit this URL in your browser to authorize:")
print()
print(f"  {auth_url}")
print()
print("  After authorizing, you'll be redirected to a localhost URL.")
print("  Copy the FULL redirect URL you were sent to (it will fail to load,")
print("  but the URL contains the authorization code).")
print()
print("  OR: If you use this tool's browser, I'll try to open it.")
print("=" * 70)

# Try to open in browser if available
try:
    import webbrowser
    webbrowser.open(auth_url)
except:
    pass

# Save URL to file for reference
with open('/tmp/oauth-url.txt', 'w') as f:
    f.write(auth_url)
print(f"\nAuth URL also saved to /tmp/oauth-url.txt")
