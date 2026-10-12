#!/usr/bin/env python3
"""Create Mad EZ Media Revenue Pipeline Google Sheet via API."""

import os
import datetime
from google.auth import default
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']

SPREADSHEET_TITLE = "Mad EZ Media — Revenue Pipeline"

PIPELINE_HEADERS = [
    "Prospect Name", "Category", "Website URL", "Is WordPress?",
    "WordPress Score", "Tier", "Contact Name", "Phone", "Email",
    "Outreach Status", "Outreach Date", "Follow-up Date", "Notes", "Assigned To"
]

CATEGORIES = ["Dental", "Holistic", "Hypnotherapy", "Wellness", "Med", "Other"]
WORDPRESS_OPTS = ["YES", "NO"]
STATUSES = ["New", "Emailed", "Called", "Demo Scheduled", "Closed", "Lost"]
ASSIGNED = ["Duane", "Mikey", "System"]

def main():
    creds, project = default(scopes=SCOPES)
    print(f"Authenticated as: {project}")

    service = build('sheets', 'v4', credentials=creds)
    drive_service = build('drive', 'v3', credentials=creds)

    # ── Step 1: Create spreadsheet ──
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

    # ── Step 2: Write headers for Revenue Pipeline ──
    pipeline_range = 'Revenue Pipeline!A1:N1'
    body = {'values': [PIPELINE_HEADERS]}
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=pipeline_range,
        valueInputOption='RAW',
        body=body
    ).execute()
    print("✓ Pipeline headers written")

    # ── Step 3: Add formulas to row 2 (demo row) ──
    # WordPress Score (E2) = IF(D2="YES",70,0)+IF(ISNUMBER(SEARCH("ai",LOWER(C2))),0,30)
    # Tier (F2) = IF(E2>=80,"HOT",IF(E2>=50,"WARM","COLD"))
    # Follow-up Date (L2) = IF(K2="","",K2+3)

    formulas_row = [
        "Example Dental Practice",  # A2
        "Dental",                   # B2
        "https://example-dental.com", # C2
        "YES",                      # D2
        '=IF(D2="YES",70,0)+IF(ISNUMBER(SEARCH("ai",LOWER(C2))),0,30)',  # E2
        '=IF(E2>=80,"HOT",IF(E2>=50,"WARM","COLD"))',  # F2
        "Dr. Smith",                # G2
        "(555) 123-4567",           # H2
        "dr.smith@example-dental.com",  # I2
        "New",                      # J2
        "",                         # K2
        '=IF(K2="","",K2+3)',       # L2
        "Introduced via website cold outreach",  # M2
        "Duane"                     # N2
    ]

    body = {'values': [formulas_row]}
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range='Revenue Pipeline!A2:N2',
        valueInputOption='USER_ENTERED',  # USER_ENTERED so formulas are interpreted
        body=body
    ).execute()
    print("✓ Demo row + formulas written")

    # ── Step 4: Expand formulas down to row 1000 ──
    # Copy formulas from row 2 down
    requests = [
        {
            "repeatCell": {
                "range": {
                    "sheetId": 0,
                    "startRowIndex": 2,  # row 3 onwards (0-indexed)
                    "endRowIndex": 1000,
                    "startColumnIndex": 4,  # E (WordPress Score)
                    "endColumnIndex": 5
                },
                "cell": {
                    "userEnteredValue": {
                        "formulaValue": '=IF(D3="YES",70,0)+IF(ISNUMBER(SEARCH("ai",LOWER(C3))),0,30)'
                    }
                },
                "fields": "userEnteredValue"
            }
        },
        {
            "repeatCell": {
                "range": {
                    "sheetId": 0,
                    "startRowIndex": 2,
                    "endRowIndex": 1000,
                    "startColumnIndex": 5,  # F (Tier)
                    "endColumnIndex": 6
                },
                "cell": {
                    "userEnteredValue": {
                        "formulaValue": '=IF(E3>=80,"HOT",IF(E3>=50,"WARM","COLD"))'
                    }
                },
                "fields": "userEnteredValue"
            }
        },
        {
            "repeatCell": {
                "range": {
                    "sheetId": 0,
                    "startRowIndex": 2,
                    "endRowIndex": 1000,
                    "startColumnIndex": 11,  # L (Follow-up Date)
                    "endColumnIndex": 12
                },
                "cell": {
                    "userEnteredValue": {
                        "formulaValue": '=IF(K3="","",K3+3)'
                    }
                },
                "fields": "userEnteredValue"
            }
        }
    ]

    body = {'requests': requests}
    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body=body
    ).execute()
    print("✓ Formulas expanded to rows 3-1000")

    # ── Step 5: Set up Weekly Targets sheet ──
    targets_data = [
        ["Metric", "Target", "Current", "Progress %", "Notes"],
        ["Daily Prospect Target", 20, 0, '=IF(B2=0,0,C2/B2)', "Duane needs 20 warm prospects/day"],
        ["Monthly Client Target", 10, 0, '=IF(B3=0,0,C3/B3)', "10 clients closed per month"],
        ["Monthly Revenue Target ($)", 5000, 0, '=IF(B4=0,0,C4/B4)', "$500/mo per client × 10 clients"],
        ["Commission Rate (%)", 10, None, None, "10% commission on closed deals"],
        ["Duane Commission Earned ($)", None, None, '=C4*(B5/100)', "Revenue × Commission Rate"],
        [],  # blank row
        ["", "", "", "", "Updated: " + datetime.date.today().strftime("%Y-%m-%d")],
    ]

    body = {'values': targets_data}
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range='Weekly Targets!A1:E8',
        valueInputOption='USER_ENTERED',
        body=body
    ).execute()
    print("✓ Weekly Targets written")

    # ── Step 6: Set up data validation (dropdowns) ──
    # Need to get the sheet IDs first
    sheet_meta = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()

    pipeline_sheet_id = None
    targets_sheet_id = None
    for s in sheet_meta['sheets']:
        if s['properties']['title'] == 'Revenue Pipeline':
            pipeline_sheet_id = s['properties']['sheetId']
        elif s['properties']['title'] == 'Weekly Targets':
            targets_sheet_id = s['properties']['sheetId']

    # Build data validation requests
    validation_requests = []

    # Category dropdown (B2:B1000)
    validation_requests.append({
        "setDataValidation": {
            "range": {
                "sheetId": pipeline_sheet_id,
                "startRowIndex": 1,
                "endRowIndex": 1000,
                "startColumnIndex": 1,
                "endColumnIndex": 2
            },
            "rule": {
                "condition": {
                    "type": "ONE_OF_LIST",
                    "values": [{"userEnteredValue": c} for c in CATEGORIES]
                },
                "showCustomUi": True,
                "strict": True
            }
        }
    })

    # Is WordPress? dropdown (D2:D1000)
    validation_requests.append({
        "setDataValidation": {
            "range": {
                "sheetId": pipeline_sheet_id,
                "startRowIndex": 1,
                "endRowIndex": 1000,
                "startColumnIndex": 3,
                "endColumnIndex": 4
            },
            "rule": {
                "condition": {
                    "type": "ONE_OF_LIST",
                    "values": [{"userEnteredValue": w} for w in WORDPRESS_OPTS]
                },
                "showCustomUi": True,
                "strict": True
            }
        }
    })

    # Outreach Status dropdown (J2:J1000)
    validation_requests.append({
        "setDataValidation": {
            "range": {
                "sheetId": pipeline_sheet_id,
                "startRowIndex": 1,
                "endRowIndex": 1000,
                "startColumnIndex": 9,
                "endColumnIndex": 10
            },
            "rule": {
                "condition": {
                    "type": "ONE_OF_LIST",
                    "values": [{"userEnteredValue": s} for s in STATUSES]
                },
                "showCustomUi": True,
                "strict": True
            }
        }
    })

    # Assigned To dropdown (N2:N1000)
    validation_requests.append({
        "setDataValidation": {
            "range": {
                "sheetId": pipeline_sheet_id,
                "startRowIndex": 1,
                "endRowIndex": 1000,
                "startColumnIndex": 13,
                "endColumnIndex": 14
            },
            "rule": {
                "condition": {
                    "type": "ONE_OF_LIST",
                    "values": [{"userEnteredValue": a} for a in ASSIGNED]
                },
                "showCustomUi": True,
                "strict": True
            }
        }
    })

    body = {'requests': validation_requests}
    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body=body
    ).execute()
    print("✓ Data validation dropdowns configured")

    # ── Step 7: Add conditional formatting ──
    if pipeline_sheet_id:
        cf_requests = []

        # Tier: HOT green, WARM yellow, COLD red
        tier_colors = [
            ("HOT", 0.6, 0.9, 0.4),   # green
            ("WARM", 0.95, 0.92, 0.5), # yellow
            ("COLD", 0.9, 0.6, 0.6),   # red
        ]
        for status, r, g, b in tier_colors:
            cf_requests.append({
                "addConditionalFormatRule": {
                    "rule": {
                        "ranges": [{
                            "sheetId": pipeline_sheet_id,
                            "startRowIndex": 1,
                            "endRowIndex": 1000,
                            "startColumnIndex": 5,
                            "endColumnIndex": 6
                        }],
                        "booleanRule": {
                            "condition": {
                                "type": "TEXT_EQ",
                                "values": [{"userEnteredValue": status}]
                            },
                            "format": {
                                "backgroundColor": {
                                    "red": r,
                                    "green": g,
                                    "blue": b
                                },
                                "textFormat": {"bold": True}
                            }
                        }
                    }
                }
            })

        # Outreach Status colors
        status_colors = [
            ("Closed", 0.6, 0.9, 0.4),    # green
            ("Lost", 0.9, 0.6, 0.6),      # red
            ("Demo Scheduled", 0.6, 0.7, 0.95),  # blue
            ("New", 0.85, 0.85, 0.95),    # light blue
        ]
        for status, r, g, b in status_colors:
            cf_requests.append({
                "addConditionalFormatRule": {
                    "rule": {
                        "ranges": [{
                            "sheetId": pipeline_sheet_id,
                            "startRowIndex": 1,
                            "endRowIndex": 1000,
                            "startColumnIndex": 9,
                            "endColumnIndex": 10
                        }],
                        "booleanRule": {
                            "condition": {
                                "type": "TEXT_EQ",
                                "values": [{"userEnteredValue": status}]
                            },
                            "format": {
                                "backgroundColor": {
                                    "red": r,
                                    "green": g,
                                    "blue": b
                                },
                                "textFormat": {"bold": True}
                            }
                        }
                    }
                }
            })

        body = {'requests': cf_requests}
        service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body=body
        ).execute()
        print("✓ Conditional formatting applied")

    # ── Step 8: Bold headers ──
    bold_requests = [
        {
            "repeatCell": {
                "range": {
                    "sheetId": pipeline_sheet_id,
                    "startRowIndex": 0,
                    "endRowIndex": 1,
                    "startColumnIndex": 0,
                    "endColumnIndex": 14
                },
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True},
                        "backgroundColor": {"red": 0.2, "green": 0.2, "blue": 0.2},
                        "backgroundColorStyle": {"rgbColor": {"red": 0.85, "green": 0.85, "blue": 0.85}}
                    }
                },
                "fields": "userEnteredFormat(textFormat,backgroundColor)"
            }
        },
        {
            "repeatCell": {
                "range": {
                    "sheetId": targets_sheet_id,
                    "startRowIndex": 0,
                    "endRowIndex": 1,
                    "startColumnIndex": 0,
                    "endColumnIndex": 5
                },
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True},
                        "backgroundColor": {"red": 0.85, "green": 0.85, "blue": 0.85}
                    }
                },
                "fields": "userEnteredFormat(textFormat,backgroundColor)"
            }
        }
    ]

    body = {'requests': bold_requests}
    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body=body
    ).execute()
    print("✓ Headers formatted (bold + gray background)")

    # ── Step 9: Set column widths ──
    # Auto-resize columns: cols with formulas should be wider
    resize_requests = [
        {
            "updateDimensionProperties": {
                "range": {
                    "sheetId": pipeline_sheet_id,
                    "dimension": "COLUMNS",
                    "startIndex": 0,
                    "endIndex": 14
                },
                "properties": {
                    "pixelSize": 180
                },
                "fields": "pixelSize"
            }
        }
    ]

    # Make some columns wider
    for col_idx, size in [(0, 250), (1, 150), (2, 300), (4, 150), (5, 100), (9, 160), (11, 140), (12, 300), (13, 120)]:
        resize_requests.append({
            "updateDimensionProperties": {
                "range": {
                    "sheetId": pipeline_sheet_id,
                    "dimension": "COLUMNS",
                    "startIndex": col_idx,
                    "endIndex": col_idx + 1
                },
                "properties": {
                    "pixelSize": size
                },
                "fields": "pixelSize"
            }
        })

    body = {'requests': resize_requests}
    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body=body
    ).execute()
    print("✓ Column widths adjusted")

    # ── Step 10: Add a note explaining the formulas ──
    note_requests = [
        {
            "updateCells": {
                "range": {
                    "sheetId": pipeline_sheet_id,
                    "startRowIndex": 0,
                    "endRowIndex": 1,
                    "startColumnIndex": 4,
                    "endColumnIndex": 5
                },
                "rows": [{
                    "values": [{
                        "note": "WordPress Score = IF(WP=YES,70,0) + IF(no 'ai' in URL,30,0). Max 100."
                    }]
                }],
                "fields": "note"
            }
        },
        {
            "updateCells": {
                "range": {
                    "sheetId": pipeline_sheet_id,
                    "startRowIndex": 0,
                    "endRowIndex": 1,
                    "startColumnIndex": 5,
                    "endColumnIndex": 6
                },
                "rows": [{
                    "values": [{
                        "note": "Tier = HOT(>=80), WARM(>=50), COLD(<50). Based on WordPress Score."
                    }]
                }],
                "fields": "note"
            }
        },
        {
            "updateCells": {
                "range": {
                    "sheetId": pipeline_sheet_id,
                    "startRowIndex": 0,
                    "endRowIndex": 1,
                    "startColumnIndex": 11,
                    "endColumnIndex": 12
                },
                "rows": [{
                    "values": [{
                        "note": "Follow-up Date = Outreach Date + 3 days. Auto-calculated."
                    }]
                }],
                "fields": "note"
            }
        }
    ]

    body = {'requests': note_requests}
    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body=body
    ).execute()
    print("✓ Formula notes added to headers")

    # ── Step 11: Share with Duane (set anyone with link can edit) ──
    # First get the current permissions
    try:
        drive_service.permissions().create(
            fileId=spreadsheet_id,
            body={
                'type': 'anyone',
                'role': 'writer',
                'allowFileDiscovery': True
            }
        ).execute()
        print("✓ Sheet shared with anyone with link (Editor access)")
    except Exception as e:
        print(f"  Note: Could not set link sharing: {e}")

    # ── Summary ──
    print(f"\n{'='*60}")
    print(f"  MAD EZ MEDIA — REVENUE PIPELINE")
    print(f"{'='*60}")
    print(f"  URL: {sheet_url}")
    print(f"  ID:  {spreadsheet_id}")
    print(f"{'='*60}")
    print(f"\nSHEETS:")
    print(f"  1. Revenue Pipeline — Full CRM pipeline with:")
    print(f"     • 14 columns with formulas, dropdowns, conditional formatting")
    print(f"     • WordPress Score (auto) + Tier (HOT/WARM/COLD)")
    print(f"     • Follow-up Date (auto: outreach + 3 days)")
    print(f"  2. Weekly Targets — Goals, progress tracking, commission")
    print(f"     • Target: 20 prospects/day")
    print(f"     • Target: $5,000/mo (10 clients × $500)")
    print(f"     • Commission: 10% of revenue")
    print(f"\nREADY FOR DUANE: Shared with edit access.")
    print(f"Duplicate shares/edits are tracked in Google Drive history.")
    print(f"\nLocal CSV template: mad-ez-media-revenue-pipeline.csv")
    print(f"Local setup guide:  mad-ez-media-pipeline-setup-guide.md")

if __name__ == '__main__':
    main()
