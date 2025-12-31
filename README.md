# 🫀 CodePulse - AI Code Analysis Tool

> Check your code's pulse - Smart quality analysis powered by AI

**By Saleh Almqati** | IT Student | Python 3.9+ | MIT License

[![GitHub](https://img.shields.io/badge/GitHub-DeftonesL-black?logo=github)](https://github.com/DeftonesL)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Saleh%20Almqati-blue?logo=linkedin)](https://linkedin.com/in/Saleh-almqati)
[![Twitter](https://img.shields.io/badge/Twitter-@Remindedwithyou-1DA1F2?logo=twitter)](https://twitter.com/Remindedwithyou)

---

## What is this?

CodePulse analyzes your code and gives you a grade (like a teacher!). It checks:
- 🔍 Code quality and structure
- 🤖 Logic issues (using AI)
- 🔒 Security vulnerabilities
- 📊 Overall project health

**Supports multiple languages**: Python, JavaScript, TypeScript, Java, C/C++, Go, Rust, and more!

**Result**: Score from 0-100 with letter grade (A+ to D) and recommendations.

---

## Supported Languages

CodePulse can analyze projects in multiple languages:

| Language | Extensions | Analysis Level |
|----------|-----------|----------------|
| **Python** | `.py` | ⭐⭐⭐ Full (AST + AI + Security) |
| **JavaScript** | `.js`, `.jsx` | ⭐⭐ Good (Structure + Security) |
| **TypeScript** | `.ts`, `.tsx` | ⭐⭐ Good (Structure + Security) |
| **Java** | `.java` | ⭐ Basic (Structure) |
| **C/C++** | `.c`, `.cpp`, `.h` | ⭐ Basic (Structure) |
| **Go** | `.go` | ⭐ Basic (Structure) |
| **Rust** | `.rs` | ⭐ Basic (Structure) |
| **Others** | 15+ more | ⭐ Detection only |

**Full support** = Complete analysis with AST, security scanning, and AI recommendations  
**Good support** = Structure analysis and security scanning  
**Basic support** = File detection and basic metrics  

> More languages coming soon! Check `examples/` directory for samples.

---

## Quick Start

### 1. Install
```bash
cd CodePulse
pip install -e .
```

### 2. Run Analysis
```bash
# Simple scan
python3 src/core/scanner.py ./your-project

# Security check
python3 src/modules/security.py ./your-project

# FULL ANALYSIS (recommended!)
python3 src/core/analyzer.py ./your-project
```

### 3. Check Report
Reports are saved in `reports/` directory:
```bash
python3 reports_manager.py list
```

---

## Main Features

### 🎯 Comprehensive Analysis
One command to analyze everything:
```bash
python3 src/core/analyzer.py ./your-project
```

**Output:**
```
CODEPULSE - COMPREHENSIVE ANALYSIS REPORT
============================================================
FINAL GRADE: 87.5/100 - A Very Good

DETAILS:
  • Code Quality: 85.0/100
  • Security: 90.0/100
  • Total Issues: 12
  • Security Vulnerabilities: 3

RECOMMENDATIONS:
  1. Fix SQL injection in database.py
  2. Add docstrings to functions
```

### 📊 Reports Manager
```bash
python3 reports_manager.py list      # List all reports
python3 reports_manager.py compare old.json new.json  # Compare
python3 reports_manager.py clean 5   # Keep last 5
```

---

## Grading System

| Score | Grade | Meaning |
|-------|-------|---------|
| 90-100 | A+ | Excellent |
| 85-89 | A | Very Good |
| 80-84 | B+ | Good |
| 75-79 | B | Fair |
| 70-74 | C+ | Needs Work |
| 60-69 | C | Weak |
| 0-59 | D | Critical |

**Formula**: `Overall = (Code Quality × 40%) + (Security × 60%)`

---

## File Structure

```
CodePulse/
├── README.md
├── setup.py
├── requirements.txt
├── reports_manager.py        # Report management
│
├── src/core/
│   ├── scanner.py           # AST scanner
│   ├── analyzer.py          # Main analyzer ⭐
│   ├── ai_engine.py         # AI integration
│   ├── advanced_metrics.py  # Advanced metrics
│   ├── code_patterns.py     # Pattern detection
│   ├── performance_analyzer.py # Performance analysis
│   └── security.py          # Security scanner
│
├── tests/                   # Unit tests
├── reports/                 # Auto-saved reports
└── docs/                    # Documentation
```

---

## Usage Examples

### Before Commit
```bash
python3 src/core/analyzer.py .
# If score > 80, commit with confidence!
```

### Track Progress
```bash
python3 reports_manager.py compare old.json new.json
```

### CI/CD
```yaml
- run: python3 src/core/analyzer.py .
```

---

## 🎓 About the Developer

I'm **Saleh Almqati**, an IT student who built CodePulse because:
- Late-night debugging sessions were killing me 😅
- Wanted to understand how professional analysis tools work
- Needed a standout project for my portfolio
- Wanted to help fellow students write better code

**Started as a learning project, evolved into something real!**

---

## 📬 Contact & Connect

- 📧 **Email**: xsll7c@gmail.com
- 💼 **LinkedIn**: [Saleh-almqati](https://linkedin.com/in/Saleh-almqati)
- 🐙 **GitHub**: [DeftonesL](https://github.com/DeftonesL)
- 🐦 **Twitter**: [@Remindedwithyou](https://twitter.com/Remindedwithyou)

**Questions? Feedback? Suggestions?**
- Open an issue on GitHub
- Send me an email
- Connect on LinkedIn

---

## ⭐ Support the Project

If CodePulse helped you:
- ⭐ Star the repository
- 🔄 Share with classmates/colleagues
- 💬 Give feedback
- 🐛 Report bugs
- 🤝 Contribute improvements

Every star motivates me to keep improving! 🙏

---

**Built with ❤️ and countless cups of coffee by an IT student**

*Healthy code, happy developers* 🫀

For detailed documentation, see the `docs/` folder.
