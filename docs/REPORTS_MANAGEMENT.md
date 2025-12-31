# Reports Management Guide

## Overview

CodePulse now automatically saves all reports to the `reports/` directory with timestamps!

## Benefits

✅ **Organized**: All reports in one place
✅ **Easy to Clean**: Delete old reports easily  
✅ **Track Progress**: Compare reports over time
✅ **No Clutter**: Reports don't mix with your code

## Automatic Saving

When you run comprehensive analysis:
```bash
pulse comprehensive ./my-project
```

Report is automatically saved as:
```
reports/comprehensive_report_20250115_143022.json
```

## Reports Manager Tool

We've included a powerful tool to manage your reports!

### List All Reports
```bash
python3 reports_manager.py list
```
Output:
```
Found 5 reports:

============================================================
Report: comprehensive_report_20250115_143022.json
============================================================
Project: /home/user/my-project
Date: 2025-01-15 14:30:22
Score: 87.5/100 - A Very Good
Files: 42 | Lines: 3,456
Issues: 12 | Security: 3
============================================================
```

### Show Latest Report
```bash
python3 reports_manager.py latest
```

### Compare Two Reports (Track Improvements!)
```bash
python3 reports_manager.py compare \
  reports/comprehensive_report_20250110_100000.json \
  reports/comprehensive_report_20250115_143022.json
```

Output:
```
REPORT COMPARISON
============================================================

OLD: comprehensive_report_20250110_100000.json
NEW: comprehensive_report_20250115_143022.json

Metric                         Old             New             Change
------------------------------------------------------------
Overall Score                  75.0            87.5            ✓ +12.5
Code Quality                   72.0            85.0            ✓ +13.0
Security Score                 78.0            90.0            ✓ +12.0
Total Issues                   25              12              ✓ -13
Security Issues                8               3               ✓ -5
Critical Issues                3               0               ✓ -3
```

### Delete Old Reports
```bash
# Keep only last 5 reports (delete others)
python3 reports_manager.py clean 5

# Keep only last 10 reports
python3 reports_manager.py clean 10
```

Output:
```
Deleting 3 old reports (keeping 5 most recent):
  ✓ Deleted: comprehensive_report_20250101_090000.json
  ✓ Deleted: comprehensive_report_20250102_090000.json
  ✓ Deleted: comprehensive_report_20250103_090000.json

Cleaned up! 3 reports deleted.
```

### Export to CSV (for Excel/Sheets)
```bash
python3 reports_manager.py export
```

Creates `reports_summary.csv`:
```csv
Date,Project,Overall Score,Grade,Code Quality,Security Score,Total Issues,Security Issues,Files,Lines
2025-01-15 14:30:22,/home/user/my-project,87.5,A Very Good,85.0,90.0,12,3,42,3456
2025-01-14 10:00:00,/home/user/my-project,75.0,B Fair,72.0,78.0,25,8,40,3200
```

## Workflow Examples

### Daily Development
```bash
# Run analysis
pulse comprehensive .

# Check if improved
python3 reports_manager.py list
```

### Before Commit
```bash
# Run analysis
pulse comprehensive .

# Compare with last week
python3 reports_manager.py compare \
  reports/comprehensive_report_20250108_*.json \
  reports/comprehensive_report_20250115_*.json
```

### Weekly Cleanup
```bash
# Every Sunday, keep only last 10 reports
python3 reports_manager.py clean 10
```

### Monthly Review
```bash
# Export all reports to CSV
python3 reports_manager.py export

# Open in Excel/Sheets for trend analysis
```

## Directory Structure

```
CodePulse/
├── reports/                           # Reports directory
│   ├── README.md                      # This guide
│   ├── comprehensive_report_20250115_143022.json
│   ├── comprehensive_report_20250114_100000.json
│   └── comprehensive_report_20250113_090000.json
├── reports_manager.py                 # Management tool
└── src/
    └── core/
        └── analyzer.py                # Auto-saves to reports/
```

## Git Integration

The `reports/` directory is in `.gitignore` by default, so reports won't be committed to your repository. This is good because:

✅ Reports are analysis outputs, not source code
✅ They can be large and change frequently
✅ Each developer should run their own analysis

## Tips

### 1. Regular Analysis
Run analysis before every commit:
```bash
# Add to pre-commit hook
pulse comprehensive .
```

### 2. Track Improvements
Compare reports weekly:
```bash
# See your progress!
python3 reports_manager.py compare old.json new.json
```

### 3. Share Results
Export to CSV and share with team:
```bash
python3 reports_manager.py export
# Email reports_summary.csv to team
```

### 4. Automate Cleanup
Add to crontab for weekly cleanup:
```bash
# Every Sunday at midnight
0 0 * * 0 cd /path/to/project && python3 reports_manager.py clean 10
```

## Troubleshooting

### "No reports found"
- Make sure you've run `pulse comprehensive` at least once
- Check you're in the right directory
- Reports are in `reports/` subdirectory

### "Report not found"
- Use full path or relative path from project root
- Use `reports_manager.py list` to see available reports

### Reports not saving
- Check write permissions on `reports/` directory
- Make sure directory exists (created automatically)

---

## Summary

**Before**: Reports scattered in project root
**Now**: All organized in `reports/` directory!

Commands to remember:
```bash
# Run analysis (auto-saves to reports/)
pulse comprehensive .

# List reports
python3 reports_manager.py list

# Compare reports
python3 reports_manager.py compare old.json new.json

# Clean old reports
python3 reports_manager.py clean 5
```

**Built with organization in mind by Saleh Almqati**
