# Getting Started with CodePulse

## 3 Steps to Start

### Step 1: Install
```bash
cd CodePulse
pip install -e .
```

### Step 2: Run
```bash
# Analyze your project
python3 src/core/analyzer.py /path/to/your-project
```

### Step 3: Check Results
```bash
# View your report
cat reports/comprehensive_report_*.json

# Or list all reports
python3 reports_manager.py list
```

---

## What You Get

After analysis, you'll see:
- **Grade**: A+ to D (like school!)
- **Score**: 0-100
- **Issues**: What needs fixing
- **Recommendations**: How to improve

---

## Commands Cheat Sheet

```bash
# Full analysis
python3 src/core/analyzer.py ./project

# Just scan
python3 src/core/scanner.py ./project

# Just security
python3 src/modules/security.py ./project

# Manage reports
python3 reports_manager.py list
python3 reports_manager.py compare old.json new.json
python3 reports_manager.py clean 5

# Demo
python3 demo.py
```

---

## Example Output

```
CODEPULSE - COMPREHENSIVE ANALYSIS REPORT
============================================================
FINAL GRADE: 87.5/100 - A Very Good
============================================================

DETAILS:
  • Code Quality: 85.0/100
  • Security: 90.0/100
  • Issues: 12
  • Vulnerabilities: 3

TOP ISSUES:
  1. [HIGH] Inefficient loop in processor.py
  2. [MEDIUM] Missing type hints in utils.py

RECOMMENDATIONS:
  1. Fix SQL injection in database.py
  2. Add docstrings to public functions
```

---

## Need Help?

- Read `README.md` - Main documentation
- Check `docs/REPORTS_MANAGEMENT.md` - Report tools
- Run `python3 demo.py` - See it in action

---

**That's it! Start analyzing your code! 🚀**

— Saleh Almqati
