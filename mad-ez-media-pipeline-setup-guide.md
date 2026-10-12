# Mad EZ Media — Revenue Pipeline
## Google Sheets Setup Guide & Formula Documentation
### For Duane (Sales Lead)

---

## OVERVIEW

This sheet is the single source of truth for the Mad EZ Media sales pipeline.
It tracks prospects through the full lifecycle — from discovery to close.

**Goal for Duane:** 20 warm prospects/day
**Monthly Target:** $5,000/mo (10 clients at $500/mo)

---

## SHEET 1: "Revenue Pipeline" — Column Reference

| # | Column | Type | Description |
|---|--------|------|-------------|
| A | Prospect Name | Text | Business/individual name |
| B | Category | Dropdown | Dental / Holistic / Hypnotherapy / Wellness / Med / Other |
| C | Website URL | Text/URL | The prospect's website |
| D | Is WordPress? | Dropdown | YES / NO |
| E | WordPress Score | Formula | Auto-calculated score (0-100) |
| F | Tier | Formula | HOT / WARM / COLD based on score |
| G | Contact Name | Text | Decision-maker name |
| H | Phone | Text | Contact phone number |
| I | Email | Text | Contact email address |
| J | Outreach Status | Dropdown | New / Emailed / Called / Demo Scheduled / Closed / Lost |
| K | Outreach Date | Date | When outreach was made |
| L | Follow-up Date | Formula | Auto-calculated = Outreach Date + 3 days |
| M | Notes | Text | Free-form notes |
| N | Assigned To | Dropdown | Duane / Mikey / System |

---

## FORMULAS

### E2 (WordPress Score)
```
=IF(D2="YES",40,0) + IF(D2="YES",30,0) + IF(ISNUMBER(SEARCH("ai",LOWER(C2))),0,30)
```
**Breakdown:**
- WordPress detected (D2="YES"): +40 points
- Old design assumption (D2="YES"): +30 points (sites on WordPress tend to have older designs)
- No AI detected in URL/content: +30 points
- **Max score: 100**

**Simplified alternative (easier to maintain):**
```
=IF(D2="YES",70,0) + IF(ISNUMBER(SEARCH("ai",LOWER(C2))),0,30)
```
This gives:
- WordPress site = 70 base (40 for WP + 30 for old design)
- Non-WordPress = 0 base
- If URL doesn't contain "ai" = +30 (ripe for AI upgrade)
- Hot prospects = WordPress + no existing AI solution

### F2 (Tier)
```
=IF(E2>=80,"HOT",IF(E2>=50,"WARM","COLD"))
```
- **HOT:** Score >= 80 — WordPress site, no AI, strong opportunity
- **WARM:** Score >= 50 — Some signals of opportunity
- **COLD:** Score < 50 — Needs more research

### L2 (Follow-up Date)
```
=IF(K2="","",K2+3)
```
- Auto-calculates 3 days after outreach date
- Stays blank if no outreach date entered yet

---

## DATA VALIDATION (Dropdowns)

### Category (Column B)
- List of items: `Dental, Holistic, Hypnotherapy, Wellness, Med, Other`

### Is WordPress? (Column D)
- List of items: `YES, NO`

### Outreach Status (Column J)
- List of items: `New, Emailed, Called, Demo Scheduled, Closed, Lost`

### Assigned To (Column N)
- List of items: `Duane, Mikey, System`

---

## HOW TO SET UP IN GOOGLE SHEETS

### Step 1: Create the Sheet
1. Go to https://sheets.google.com
2. Click **+ Blank** to create a new spreadsheet
3. Rename the spreadsheet: **"Mad EZ Media — Revenue Pipeline"**
4. Rename Sheet1 to **"Revenue Pipeline"**
5. Click **+** to add a new sheet, rename it to **"Weekly Targets"**

### Step 2: Set Up Headers (Revenue Pipeline sheet)
Copy this row into Row 1:
```
Prospect Name | Category | Website URL | Is WordPress? | WordPress Score | Tier | Contact Name | Phone | Email | Outreach Status | Outreach Date | Follow-up Date | Notes | Assigned To
```

### Step 3: Add Formulas
- **E2:** `=IF(D2="YES",70,0)+IF(ISNUMBER(SEARCH("ai",LOWER(C2))),0,30)`
- **F2:** `=IF(E2>=80,"HOT",IF(E2>=50,"WARM","COLD"))`
- **L2:** `=IF(K2="","",K2+3)`
- **Drag down** all three formulas to fill the column (Google Sheets auto-adjusts row numbers)

### Step 4: Add Data Validation (Dropdowns)
For each column, do:
1. Select the column (or the data range, e.g., B2:B1000)
2. Click **Data → Data validation**
3. Choose **List of items**
4. Enter the comma-separated values listed above
5. Click **Save**

### Step 5: Set Up Weekly Targets Sheet

| A | B | C | D | E |
|---|---|---|---|---|
| Metric | Target | Current | Progress % | Notes |
| Daily Prospect Target | 20 | 0 | =IF(B2=0,0,C2/B2)*100 | Duane needs 20 warm prospects/day |
| Monthly Client Target | 10 | 0 | =IF(B3=0,0,C3/B3)*100 | 10 clients closed per month |
| Monthly Revenue Target ($) | 5000 | 0 | =IF(B4=0,0,C4/B4)*100 | $500/mo per client × 10 clients |
| Commission Rate (%) | 10 | | | 10% commission on closed deals |
| Duane Commission Earned ($) | | 0 | =C4*(B5/100) | Revenue × Commission Rate |

### Step 6: Conditional Formatting (Optional but Recommended)

**Tier column (F):**
- If text contains "HOT" → **Green** background
- If text contains "WARM" → **Yellow** background
- If text contains "COLD" → **Red** background

**Outreach Status (J):**
- "Closed" → Green
- "Lost" → Red
- "New" → Blue
- "Demo Scheduled" → Purple

### Step 7: Share with Duane
1. Click **Share** (top-right)
2. Enter Duane's email
3. Set permission: **Editor**
4. Add a note: "Mad EZ Media pipeline — let's crush it!"

---

## COMMISSION TRACKING

Duane's commission structure:
- **10% commission** on every closed deal
- Monthly Revenue Target: $5,000 (10 clients × $500/mo average)
- Commission Earned = Total Revenue × 10%

**To track per deal:**
1. When a prospect reaches "Closed" status in Outreach Status (J)
2. Add the deal value in Notes (M): `$500 - signed 6mo contract`
3. The Weekly Targets sheet calculates total commission based on revenue

---

## PROSPECT PIPELINE WORKFLOW

```
Discovery → Add to Sheet (New) → Research → Score → Tier → 
Outreach (Emailed/Called) → Follow-up (3 days later) → 
Demo Scheduled → Negotiate → Closed (✓) or Lost (✗)
```

**Duane's Daily Workflow:**
1. Open the sheet every morning
2. Filter by "New" — prioritize HOT and WARM prospects
3. Make outreach calls/emails
4. Update Outreach Status and Outreach Date
5. Check Follow-up Date column for overdue follow-ups
6. Add 20 new prospects minimum per day

---

## FILE REFERENCE

This documentation accompanies the CSV template files:

- **`mad-ez-media-revenue-pipeline.csv`** — Main pipeline sheet (sample rows)
- **`mad-ez-media-weekly-targets.csv`** — Weekly targets & commission tracker

To import CSV into Google Sheets:
1. File → Import → Upload → Select CSV
2. Choose "Replace current sheet" or "New sheet"
3. Click Import
4. Then add the formulas and data validation manually (see steps above)

---

*Generated for Mad EZ Media — Autonomous Revenue Engine*
*Agent: Hermes Agent | Date: June 4, 2026*
