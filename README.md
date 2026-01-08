
# CodePulse -  Code Intelligence & Security Scanner

**Version:** 0.10.1  
**Author:** Saleh Almqati  
**License:** MIT  
**Status:** Production Ready
=======
# CodePulse - Deep Code Intelligence Engine

> Advanced static analysis tool for Python and 13+ programming languages

**Version:** 0.7.1 | **License:** MIT | **Python:** 3.9+

[![Version](https://img.shields.io/badge/version-0.7.1-blue.svg)](https://github.com/DeftonesL/CodePulse)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)


---

## Overview


CodePulse is a comprehensive static code analysis tool designed for professional code intelligence and security scanning. It supports 25+ programming languages and provides detailed HTML reports with security vulnerability detection, code quality analysis, and performance metrics.

---

## Key Features

### Multi-Language Support
- **Programming Languages:** Python, JavaScript, TypeScript, Java, C, C++, C#, Go, Rust, Ruby, PHP, Swift, Kotlin, Scala, R, Dart, Lua, Shell
- **Web Technologies:** HTML, CSS, SCSS, SASS, XML
- **Data Formats:** JSON, YAML, SQL, Markdown
- **Total:** 25+ file types supported

### Analysis Capabilities
- **Security Scanning:** OWASP vulnerability patterns, SQL injection detection, XSS vulnerabilities, hardcoded credentials
- **Code Quality:** Complexity metrics, code smells, best practice violations
- **Performance Analysis:** Parallel processing, smart caching, incremental scanning
- **Deep Analysis:** Control Flow Graphs (CFG), Data Flow Graphs (DFG), Call Graph analysis
- **Clone Detection:** Duplicate code identification across projects

### Reporting
- **HTML Reports:** Interactive dashboards with visual analytics
- **JSON Export:** Machine-readable output for CI/CD integration
- **Comprehensive Metrics:** Files analyzed, issues found, quality scores, performance statistics

### Performance
- **Parallel Processing:** 10x faster than sequential scanning
- **Smart Caching:** 60x performance improvement on repeated scans
- **Incremental Analysis:** 20x faster when scanning only changed files
- **Scalability:** Tested on projects with 10,000+ files

---

## Installation

### Requirements
- Python 3.9 or higher
- pip package manager

### Dependencies
```
click>=8.0.0
rich>=13.0.0
networkx>=3.0
jinja2>=3.1.0
pytest>=8.0.0
pytest-cov>=4.1.0
black>=24.0.0
mypy>=1.8.0
```

### Setup
```bash
# Windows
.\codepulse install

# Linux/Mac
./codepulse.sh install

# Manual installation
pip install -r requirements.txt
```

---

## Usage

### Command Line Interface

#### Scanning Commands
```bash
# Basic scan with HTML report
.\codepulse scan <project_path>

# Fast mode with 8 parallel workers
.\codepulse fast <project_path>

# Full scan without cache
.\codepulse full <project_path>

# JSON output for automation
.\codepulse json <project_path>

# Comprehensive deep analysis
.\codepulse comprehensive <project_path>
```

#### Project Management
```bash
# Install dependencies
.\codepulse install

# Run test suite
.\codepulse test

# Performance benchmark
.\codepulse benchmark

# Clean cache and reports
.\codepulse clean

# View reports directory
.\codepulse reports

# Display help menu
.\codepulse help
```

### Direct Python Usage
```bash
# Custom scan with specific options
python fast_scan.py <path> --format html --workers 16

# Specific file pattern
python fast_scan.py <path> --pattern "*.js"

# Disable caching
python fast_scan.py <path> --no-cache

# Custom output location
python fast_scan.py <path> --output custom_report.html
```

---

## Report Features

### HTML Dashboard
- **Summary Statistics:** Total files, issues count, security vulnerabilities, quality score
- **Issue Breakdown:** Categorized by type (Security/Quality) with detailed descriptions
- **File Analysis:** Complete file listing with metrics and status indicators
- **Visual Design:** Modern dark theme optimized for readability
- **Animations:** Smooth transitions and interactive elements
- **Responsive:** Compatible with desktop and mobile devices

### Metrics Provided
- Total files analyzed
- Lines of code
- Function count
- Class count
- Security issues detected
- Quality issues identified
- Overall quality score (0-100%)
- Scan duration
- Cache efficiency

---

## Performance Benchmarks

### Scan Speed
| File Count | Sequential | Parallel (8 workers) | With Cache | Incremental |
|-----------|-----------|---------------------|-----------|-------------|
| 10 files | 1.0s | 0.2s | 0.1s | 0.1s |
| 100 files | 60.0s | 6.0s | 1.0s | 3.0s |
| 1000 files | 600.0s | 60.0s | 8.0s | 30.0s |

### Performance Improvements
- **Parallel Processing:** 10x faster than sequential
- **Smart Caching:** 60x faster on repeat scans
- **Incremental Analysis:** 20x faster for changed files only

---

## Supported File Extensions

### Programming Languages
```
.py, .pyw          - Python
.js, .jsx, .mjs    - JavaScript
.ts, .tsx          - TypeScript
.java              - Java
.c, .h             - C
.cpp, .cc, .cxx    - C++
.cs                - C#
.go                - Go
.rs                - Rust
.rb                - Ruby
.php               - PHP
.swift             - Swift
.kt, .kts          - Kotlin
.scala             - Scala
.r                 - R
.dart              - Dart
.lua               - Lua
.sh, .bash         - Shell
```

### Web and Data
```
.html, .htm        - HTML
.css, .scss, .sass - CSS
.xml               - XML
.json              - JSON
.yml, .yaml        - YAML
.sql               - SQL
.md                - Markdown
```

---

## Configuration

### Command Line Options
```
--workers N           Number of parallel workers (default: CPU count)
--no-cache           Disable result caching
--no-incremental     Analyze all files (ignore modification time)
--clear-cache        Clear cache before scanning
--reset              Reset incremental state
--pattern PATTERN    File pattern to scan (default: *)
--output FILE        Output file path
--format FORMAT      Output format: json or html (default: json)
```

### Performance Tuning
```bash
# Maximum parallelization
python fast_scan.py <path> --workers 16

# Force fresh scan
python fast_scan.py <path> --no-cache --no-incremental

# Specific file types only
python fast_scan.py <path> --pattern "*.py"
```

---

## Integration

### CI/CD Pipeline
```yaml
# Example GitHub Actions workflow
- name: Code Analysis
  run: |
    pip install -r requirements.txt
    python fast_scan.py ./src --format json
    # Parse JSON output for quality gates
```

### Build Scripts
```bash
# Pre-commit hook
python fast_scan.py ./src --format json --output scan_results.json
if [ $(jq '.stats.total_issues' scan_results.json) -gt 0 ]; then
    exit 1
fi
=======
CodePulse is a comprehensive code analysis tool that combines security scanning, code quality assessment, clone detection, and performance analysis. Unlike traditional linters, CodePulse performs deep semantic analysis using graph-based algorithms and custom metrics.

### Key Capabilities

- **Security Analysis**: OWASP Top 10 vulnerability detection across 13+ languages
- **Code Quality**: Intelligent smell detection with minimal false positives
- **Clone Detection**: AST-based duplicate code identification (Type 1-4 clones)
- **Performance Analysis**: Algorithmic complexity detection and optimization suggestions
- **Multi-Language Support**: Python, JavaScript, TypeScript, PHP, Java, C#, Go, Ruby, Rust, Kotlin, HTML, JSON, SQL

---

## Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/DeftonesL/CodePulse.git
cd CodePulse

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import src.core.scanner; print('Ready')"
```

### Basic Usage

```bash
# Scan single file
python comprehensive_scan.py path/to/file.py

# Scan entire project
python comprehensive_scan.py ./project

# View reports
ls reports/

```

---


## Architecture

### Core Components
- **Scanner Engine:** Multi-threaded file processor with AST analysis
- **Cache System:** SHA-256 based result caching
- **Incremental Analyzer:** Modification time tracking for changed files
- **Security Scanner:** Pattern-based vulnerability detection
- **Quality Analyzer:** Code metrics and smell detection
- **Report Generator:** HTML and JSON output formatters

### Analysis Pipeline
1. File discovery and filtering
2. Incremental change detection
3. Parallel processing with worker pool
4. Cache lookup/store
5. Result aggregation
6. Report generation

---

## Testing

### Run Test Suite
```bash
# All tests
.\codepulse test

# Specific test file
python -m pytest tests/test_scanner.py -v

# With coverage
python -m pytest tests/ --cov=src --cov-report=html
```

### Test Coverage
- Unit tests for core components
- Integration tests for scan pipeline
- Performance benchmarks
- Target coverage: 80%+
=======
## Core Features

### 1. Security Scanner

Detects vulnerabilities including:
- SQL Injection (CWE-89)
- Cross-Site Scripting (CWE-79)
- Path Traversal (CWE-22)
- Command Injection (CWE-78)
- Hardcoded Credentials (CWE-798)
- Weak Cryptography (CWE-327)
- And 150+ additional patterns

**Supported Languages:** Python, JavaScript, TypeScript, PHP, Java, C#, Go, Ruby, Rust, Kotlin, HTML, JSON, SQL

### 2. Code Quality Analysis

Intelligent detection with reduced false positives:
- Code smells (Bloaters, Couplers, Change Preventers)
- Complexity metrics (Cyclomatic, Cognitive, Halstead)
- Maintainability Index calculation
- Technical debt estimation

**Thresholds (v0.7):**
- Long Method: 80 lines (realistic)
- Large Class: 500 lines
- Feature Envy: Ignores standard library modules

### 3. Clone Detection

Advanced duplicate code detection:
- Type 1: Exact clones (identical code)
- Type 2: Renamed clones (same structure, different names)
- Type 3: Modified clones (with minor changes)
- Type 4: Semantic clones (same functionality, different implementation)

**Minimum Thresholds:**
- Cross-file clones: 10 lines
- Same-file clones: 15 lines

### 4. Performance Analysis

Algorithmic complexity detection:
- O(n²) nested loop detection
- O(n³) triple-nested loops
- Memory leak patterns
- Inefficient operations
- N+1 query detection

---

## Output Reports

### Report Format

Reports are saved in `reports/` directory as JSON:

```json
{
  "project_score": 68.5,
  "grade": "C+",
  "total_issues": {
    "security": 35,
    "smells": 52,
    "clones": 8,
    "performance": 31
  },
  "files": {
    "path/to/file.py": {
      "security_issues": [...],
      "code_smells": [...],
      "clones": [...],
      "performance_issues": [...]
    }
  }
}
```

### Score Interpretation

- **90-100 (A)**: Excellent code quality
- **80-89 (B)**: Good code with minor issues
- **70-79 (C)**: Acceptable, needs improvement
- **60-69 (D)**: Below standard, requires attention
- **0-59 (F)**: Critical issues, immediate action needed


---

## Documentation


- **Quick Start:** QUICK_START.md
- **Technical Architecture:** docs/TECHNICAL_ARCHITECTURE.md
- **Performance Features:** docs/PERFORMANCE_FEATURES.md
- **Contributing Guidelines:** CONTRIBUTING.md
- **Changelog:** CHANGELOG.md

---

## Version History

### v0.10.1 (2026-01-08)
- Enhanced HTML reports with advanced animations
- Full error display (Security and Quality issues)
- Extended language support to 25+ file types
- Fixed comprehensive scan compatibility
- Updated default scan pattern to include all files

### v0.10.0 (2026-01-07)
- Introduced HTML report generation
- Added cross-platform launcher scripts
- Implemented multi-language support
- Performance optimizations (parallel, cache, incremental)

### v0.9.0 (2026-01-06)
- Multi-language analysis support
- Performance optimization modules

### v0.8.0 (2026-01-05)
- Deep analysis capabilities
- Clone and smell detection

---

## System Requirements

### Minimum
- CPU: Dual-core processor
- RAM: 2GB available memory
- Storage: 100MB for installation
- Python: 3.9+

### Recommended
- CPU: Quad-core or higher
- RAM: 4GB+ available memory
- Storage: 500MB for cache and reports
- Python: 3.11+

---

## Support

### Issues and Bugs
Report issues at: https://github.com/DeftonesL/CodePulse/issues

### Contributing
See CONTRIBUTING.md for contribution guidelines

### Contact
- GitHub: @DeftonesL
- Repository: https://github.com/DeftonesL/CodePulse
=======
### Essential Guides

- [QUICK_START.md](QUICK_START.md) - Get started in 5 minutes
- [COMPREHENSIVE_GUIDE.md](COMPREHENSIVE_GUIDE.md) - Complete usage guide
- [PYTHON_VERSION_GUIDE.md](PYTHON_VERSION_GUIDE.md) - Python compatibility

### Technical Documentation

- [docs/TECHNICAL_ARCHITECTURE.md](docs/TECHNICAL_ARCHITECTURE.md) - System design
- [docs/ADVANCED_FEATURES.md](docs/ADVANCED_FEATURES.md) - Advanced capabilities
- [docs/REPORTS_MANAGEMENT.md](docs/REPORTS_MANAGEMENT.md) - Working with reports

### Release Notes

- [CHANGELOG.md](CHANGELOG.md) - Version history
- [IMPROVEMENTS.md](IMPROVEMENTS.md) - v0.7 improvements
- [CRITICAL_FIXES.md](CRITICAL_FIXES.md) - v0.7.1 bug fixes

---

## Language Support

### Full Analysis
- Python (complete feature set)

### Security Scanning  
- JavaScript, TypeScript
- PHP, Java, C#
- Go, Ruby, Rust, Kotlin
- HTML, JSON, SQL

---

## Requirements

**System:**
- Python 3.9+
- 4 GB RAM minimum
- 100 MB disk space

**Dependencies:**
- networkx>=3.0
- click>=8.0.0
- rich>=13.0.0

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.


---

## License

MIT License - See LICENSE file for details

Copyright (c) 2026 Saleh Almqati

---

## Acknowledgments

- Built with Python AST analysis
- HTML reporting powered by Jinja2
- Performance profiling with pytest-benchmark
- Code metrics inspired by industry standards (OWASP, CWE)

---

**CodePulse - Professional Code Analysis Made Simple**

Version 0.10.1 | Production Ready | MIT Licensed
=======
MIT License - see [LICENSE](LICENSE) file.

---

## Contact

**Author:** Saleh Almqati  
**GitHub:** [@DeftonesL](https://github.com/DeftonesL)  
---

**CodePulse v0.7.1** - Professional code analysis for serious developers.

