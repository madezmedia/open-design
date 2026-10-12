#!/usr/bin/env python3
"""OAuth + Create Sheet — runs local server for redirect capture."""

import json
import os
import socket
import threading
import time
from urllib.parse import urlparse, parse_qs
import http.server

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

import datetime

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
]

TOKEN_FILE = '/tmp/gsheets-token.json'

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

def get_creds():
    """Try to load existing token or run OAuth flow."""
    creds = None
    
    # Check for existing token
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE) as f:
            token_data = json.load(f)
        from google.oauth2.credentials import Credentials
        creds = Credentials.from_authorized_user_info(token_data, SCOPES)
    
    # If creds exist but expired, refresh
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(TOKEN_FILE, 'w') as f:
            f.write(creds.to_json())
        print("✓ Token refreshed")
        return creds
    
    # Need new token
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_config(CLIENT_CONFIG, SCOPES)
        creds = flow.run_local_server(port=0, open_browser=False)
        with open(TOKEN_FILE, 'w') as f:
            f.write(creds.to_json())
        print("✓ New token obtained")
        return creds
    
    return creds


def create_pipeline_sheet(creds):
    """Create the full pipeline spreadsheet."""
    service = build('sheets', 'v4', credentials=creds)
    drive_service = build('drive', 'v3', credentials=creds)
    
    SPREADSHEET_TITLE = "Mad EZ Media — Revenue Pipeline"
    
    CATEGORIES = ["Dental", "Holistic", "Hypnotherapy", "Wellness", "Med", "Other"]
    WORDPRESS_OPTS = ["YES", "NO"]
    STATUSES = ["New", "Emailed", "Called", "Demo Scheduled", "Closed", "Lost"]
    ASSIGNED = ["Duane", "Mikey", "System"]
    
    PIPELINE_HEADERS = [
        "Prospect Name", "Category", "Website URL", "Is WordPress?",
        "WordPress Score", "Tier", "Contact Name", "Phone", "Email",
        "Outreach Status", "Outreach Date", "Follow-up Date", "Notes", "Assigned To"
    ]
    
    # Create spreadsheet
    spreadsheet_body = {
        'properties': {
            'title': SPREADSHEET_TITLE,
            'locale': 'en_US',
            'timeZone': 'America/New_York',
        },
        'sheets': [
            {'properties': {'title': 'Revenue Pipeline', 'gridProperties': {'frozenRowCount': 1}}},
            {'properties': {'title': 'Weekly Targets'}},
        ]
    }
    
    sheet = service.spreadsheets().create(body=spreadsheet_body).execute()
    spreadsheet_id = sheet['spreadsheetId']
    sheet_url = sheet['spreadsheetUrl']
    print(f"✓ Created spreadsheet: {sheet_url}")
    
    # Write headers
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range='Revenue Pipeline!A1:N1',
        valueInputOption='RAW',
        body={'values': [PIPELINE_HEADERS]}
    ).execute()
    print("✓ Headers written")
    
    # Write demo row with formulas
    demo_row = [
        "Example Dental Practice",
        "Dental",
        "https://example-dental.com",
        "YES",
        '=IF(D2="YES",70,0)+IF(ISNUMBER(SEARCH("ai",LOWER(C2))),0,30)',
        '=IF(E2>=80,"HOT",IF(E2>=50,"WARM","COLD"))',
        "Dr. Smith",
        "(555) 123-4567",
        "dr.smith@example-dental.com",
        "New",
        "",
        '=IF(K2="","",K2+3)',
        "Introduced via website cold outreach",
        "Duane"
    ]
    
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range='Revenue Pipeline!A2:N2',
        valueInputOption='USER_ENTERED',
        body={'values': [demo_row]}
    ).execute()
    print("✓ Demo row + formulas written")
    
    # Get sheet IDs
    sheet_meta = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    pipeline_sheet_id = None
    targets_sheet_id = None
    for s in sheet_meta['sheets']:
        if s['properties']['title'] == 'Revenue Pipeline':
            pipeline_sheet_id = s['properties']['sheetId']
        elif s['properties']['title'] == 'Weekly Targets':
            targets_sheet_id = s['properties']['sheetId']
    
    # Expand formulas to rows 3-1000
    formula_requests = [
        {
            "repeatCell": {
                "range": {"sheetId": pipeline_sheet_id, "startRowIndex": 2, "endRowIndex": 1000,
                          "startColumnIndex": 4, "endColumnIndex": 5},
                "cell": {"userEnteredValue": {"formulaValue": '=IF(D3="YES",70,0)+IF(ISNUMBER(SEARCH("ai",LOWER(C3))),0,30)'}},
                "fields": "userEnteredValue"
            }
        },
        {
            "repeatCell": {
                "range": {"sheetId": pipeline_sheet_id, "startRowIndex": 2, "endRowIndex": 1000,
                          "startColumnIndex": 5, "endColumnIndex": 6},
                "cell": {"userEnteredValue": {"formulaValue": '=IF(E3>=80,"HOT",IF(E3>=50,"WARM","COLD"))'}},
                "fields": "userEnteredValue"
            }
        },
        {
            "repeatCell": {
                "range": {"sheetId": pipeline_sheet_id, "startRowIndex": 2, "endRowIndex": 1000,
                          "startColumnIndex": 11, "endColumnIndex": 12},
                "cell": {"userEnteredValue": {"formulaValue": '=IF(K3="","",K3+3)'}},
                "fields": "userEnteredValue"
            }
        }
    ]
    
    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={'requests': formula_requests}
    ).execute()
    print("✓ Formulas expanded to rows 3-1000")
    
    # Weekly Targets
    targets_data = [
        ["Metric", "Target", "Current", "Progress %", "Notes"],
        ["Daily Prospect Target", 20, 0, '=IF(B2=0,0,C2/B2)', "Duane needs 20 warm prospects/day"],
        ["Monthly Client Target", 10, 0, '=IF(B3=0,0,C3/B3)', "10 clients closed per month"],
        ["Monthly Revenue Target ($)", 5000, 0, '=IF(B4=0,0,C4/B4)', "$500/mo per client × 10 clients"],
        ["Commission Rate (%)", 10, None, None, "10% commission on closed deals"],
        ["Duane Commission Earned ($)", None, None, '=C4*(B5/100)', "Revenue × Commission Rate"],
        [],
        ["", "", "", "", "Updated: " + datetime.date.today().strftime("%Y-%m-%d")],
    ]
    
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range='Weekly Targets!A1:E8',
        valueInputOption='USER_ENTERED',
        body={'values': targets_data}
    ).execute()
    print("✓ Weekly Targets written")
    
    # Data validation dropdowns
    validations = [
        (1, 2, [{"userEnteredValue": c} for c in CATEGORIES]),      # B: Category
        (3, 4, [{"userEnteredValue": w} for w in WORDPRESS_OPTS]),  # D: WordPress
        (9, 10, [{"userEnteredValue": s} for s in STATUSES]),       # J: Outreach Status
        (13, 14, [{"userEnteredValue": a} for a in ASSIGNED]),      # N: Assigned To
    ]
    
    val_requests = []
    for start_col, end_col, values in validations:
        val_requests.append({
            "setDataValidation": {
                "range": {
                    "sheetId": pipeline_sheet_id,
                    "startRowIndex": 1, "endRowIndex": 1000,
                    "startColumnIndex": start_col, "endColumnIndex": end_col
                },
                "rule": {
                    "condition": {"type": "ONE_OF_LIST", "values": values},
                    "showCustomUi": True,
                    "strict": True
                }
            }
        })
    
    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={'requests': val_requests}
    ).execute()
    print("✓ Dropdowns configured")
    
    # Conditional formatting
    cf_requests = []
    
    # Tier colors
    for status, r, g, b in [("HOT", 0.6, 0.9, 0.4), ("WARM", 0.95, 0.92, 0.5), ("COLD", 0.9, 0.6, 0.6)]:
        cf_requests.append({
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [{"sheetId": pipeline_sheet_id, "startRowIndex": 1, "endRowIndex": 1000,
                                "startColumnIndex": 5, "endColumnIndex": 6}],
                    "booleanRule": {
                        "condition": {"type": "TEXT_EQ", "values": [{"userEnteredValue": status}]},
                        "format": {"backgroundColor": {"red": r, "green": g, "blue": b}, "textFormat": {"bold": True}}
                    }
                }
            }
        })
    
    # Status colors
    for status, r, g, b in [("Closed", 0.6, 0.9, 0.4), ("Lost", 0.9, 0.6, 0.6),
                             ("Demo Scheduled", 0.6, 0.7, 0.95), ("New", 0.85, 0.85, 0.95)]:
        cf_requests.append({
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [{"sheetId": pipeline_sheet_id, "startRowIndex": 1, "endRowIndex": 1000,
                                "startColumnIndex": 9, "endColumnIndex": 10}],
                    "booleanRule": {
                        "condition": {"type": "TEXT_EQ", "values": [{"userEnteredValue": status}]},
                        "format": {"backgroundColor": {"red": r, "green": g, "blue": b}, "textFormat": {"bold": True}}
                    }
                }
            }
        })
    
    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={'requests': cf_requests}
    ).execute()
    print("✓ Conditional formatting applied")
    
    # Format headers
    format_requests = [
        {
            "repeatCell": {
                "range": {"sheetId": pipeline_sheet_id, "startRowIndex": 0, "endRowIndex": 1,
                          "startColumnIndex": 0, "endColumnIndex": 14},
                "cell": {"userEnteredFormat": {
                    "textFormat": {"bold": True},
                    "backgroundColor": {"red": 0.85, "green": 0.85, "blue": 0.85}
                }},
                "fields": "userEnteredFormat(textFormat,backgroundColor)"
            }
        },
        {
            "repeatCell": {
                "range": {"sheetId": targets_sheet_id, "startRowIndex": 0, "endRowIndex": 1,
                          "startColumnIndex": 0, "endColumnIndex": 5},
                "cell": {"userEnteredFormat": {
                    "textFormat": {"bold": True},
                    "backgroundColor": {"red": 0.85, "green": 0.85, "blue": 0.85}
                }},
                "fields": "userEnteredFormat(textFormat,backgroundColor)"
            }
        }
    ]
    
    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={'requests': format_requests}
    ).execute()
    print("✓ Headers formatted")
    
    # Column widths
    width_requests = [
        {"updateDimensionProperties": {
            "range": {"sheetId": pipeline_sheet_id, "dimension": "COLUMNS", "startIndex": 0, "endIndex": 1},
            "properties": {"pixelSize": 250}, "fields": "pixelSize"
        }},
        {"updateDimensionProperties": {
            "range": {"sheetId": pipeline_sheet_id, "dimension": "COLUMNS", "startIndex": 1, "endIndex": 2},
            "properties": {"pixelSize": 150}, "fields": "pixelSize"
        }},
        {"updateDimensionProperties": {
            "range": {"sheetId": pipeline_sheet_id, "dimension": "COLUMNS", "startIndex": 2, "endIndex": 3},
            "properties": {"pixelSize": 300}, "fields": "pixelSize"
        }},
        {"updateDimensionProperties": {
            "range": {"sheetId": pipeline_sheet_id, "dimension": "COLUMNS", "startIndex": 4, "endIndex": 5},
            "properties": {"pixelSize": 150}, "fields": "pixelSize"
        }},
        {"updateDimensionProperties": {
            "range": {"sheetId": pipeline_sheet_id, "dimension": "COLUMNS", "startIndex": 11, "endIndex": 12},
            "properties": {"pixelSize": 140}, "fields": "pixelSize"
        }},
        {"updateDimensionProperties": {
            "range": {"sheetId": pipeline_sheet_id, "dimension": "COLUMNS", "startIndex": 12, "endIndex": 13},
            "properties": {"pixelSize": 300}, "fields": "pixelSize"
        }},
    ]
    
    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={'requests': width_requests}
    ).execute()
    print("✓ Column widths set")
    
    # Share with anyone with link
    try:
        drive_service.permissions().create(
            fileId=spreadsheet_id,
            body={'type': 'anyone', 'role': 'writer', 'allowFileDiscovery': True}
        ).execute()
        print("✓ Sheet shared (anyone with link = Editor)")
    except Exception as e:
        print(f"  Note: Sharing limited: {e}")
    
    # Generate sharing link for Duane specifically
    try:
        # Create a shorter link
        short_link = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit"
        print(f"\n  → Duane share link: {short_link}")
    except:
        pass
    
    print(f"\n{'='*60}")
    print(f"  MAD EZ MEDIA — REVENUE PIPELINE")
    print(f"{'='*60}")
    print(f"  URL: {sheet_url}")
    print(f"  ID:  {spreadsheet_id}")
    print(f"{'='*60}")
    print()
    print("SHEET 1: Revenue Pipeline")
    print("  • 14 columns with formulas, dropdowns, conditional formatting")
    print("  • WordPress Score = IF(WP+old design=70) + IF(no AI=30)")
    print("  • Tier = HOT(>=80) / WARM(>=50) / COLD(<50)")
    print("  • Follow-up Date = Outreach + 3 days (auto)")
    print()
    print("SHEET 2: Weekly Targets")
    print("  • Daily: 20 prospects | Monthly: $5,000 / 10 clients")
    print("  • Commission tracking: 10% of revenue")
    print()
    print("Local backup files:")
    print("  mad-ez-media-revenue-pipeline.csv")
    print("  mad-ez-media-weekly-targets.csv")
    print("  mad-ez-media-pipeline-setup-guide.md")


if __name__ == '__main__':
    print("Starting Google Sheets OAuth flow...\n")
    creds = get_creds()
    if creds:
        create_pipeline_sheet(creds)
