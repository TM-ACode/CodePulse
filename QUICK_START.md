# Quick Start Guide

Get started with CodePulse in 5 minutes.

## Installation

```bash
# Clone
git clone https://github.com/DeftonesL/CodePulse.git
cd CodePulse

# Install
pip install -e .

# Verify
python -c "import src.core.scanner; print('✓ Ready')"
```

## Basic Usage

### 1. Analyze Single File

```bash
python3 -m src.core.scanner path/to/file.py
```

**Output:**
```
Scanning: file.py
Language: Python
Lines: 142
Functions: 8
Classes: 2
Quality Score: 85/100 (B+)
```

### 2. Deep Analysis

```bash
python3 src/core/deep_analysis.py path/to/file.py
```

**Shows:**
- Control Flow Graph analysis
- Data Flow dependencies
- Unreachable code
- Infinite loops
- Complexity metrics

### 3. Find Code Clones

```bash
python3 src/core/clone_detection.py path/to/file.py
```

**Detects:**
- Type 1: Exact copies
- Type 2: Renamed variables
- Type 3: Modified code
- Type 4: Semantic clones

### 4. Code Smell Detection

```bash
python3 src/core/smell_detector.py path/to/file.py
```

**Finds:**
- Long methods
- God classes
- Feature envy
- Dead code
- High coupling

### 5. Comprehensive Analysis

```bash
python3 src/core/analyzer.py ./project_directory
```

**Full Report:**
- All analysis types
- Cross-file architecture
- Quality trends
- Actionable recommendations

## Example Output

```
════════════════════════════════════════════════════════════════
🫀 CODEPULSE - DEEP CODE INTELLIGENCE
════════════════════════════════════════════════════════════════

PROJECT: MyApp
FILES: 42 | LINES: 5,234

OVERALL HEALTH: 82.5/100 (B+)

────────────────────────────────────────────────────────────────
📊 DEEP ANALYSIS
────────────────────────────────────────────────────────────────
Control Flow:
  ✓ Execution paths: 1,247
  ⚠ Unreachable code: 3 blocks
  ⚠ Infinite loops: 1 detected

Data Flow:
  ✓ Variables: 456
  ⚠ Unused: 23

────────────────────────────────────────────────────────────────
🔍 CLONE DETECTION
────────────────────────────────────────────────────────────────
Total Clones: 15
Duplicated Lines: 487 (9.3%)

Top Clone:
  📄 database.py:45-98 ↔ cache.py:120-173
  📏 54 lines duplicated
  💡 Extract to shared utility

────────────────────────────────────────────────────────────────
👃 CODE SMELLS
────────────────────────────────────────────────────────────────
Health: 78/100

Critical:
  1. [HIGH] Long Method - processData() (156 lines)
     💡 Extract 4 smaller methods
  
  2. [HIGH] God Class - UserManager (34 methods)
     💡 Split into Repository, Validator, Service

────────────────────────────────────────────────────────────────
🎯 RECOMMENDATIONS
────────────────────────────────────────────────────────────────
1. ⚡ Fix infinite loop (scheduler.py:234)
2. 🔴 Refactor UserManager (violates SRP)
3. 🟡 Remove 487 lines duplication
```

## Advanced Features

### Cross-File Analysis

```bash
python3 src/core/cross_file_analysis.py ./project
```

Analyzes:
- Architecture quality
- Circular dependencies
- Module coupling
- Stability metrics

### Quality Trends

```bash
python3 src/core/quality_trends.py add
```

Tracks:
- Quality over time
- Improvement trends
- Code growth patterns

## Configuration

Create `codepulse.config.json`:

```json
{
  "min_clone_lines": 6,
  "max_method_length": 50,
  "max_complexity": 10,
  "excluded_dirs": ["tests", "venv"]
}
```

## Next Steps

1. Read [TECHNICAL_ARCHITECTURE.md](docs/TECHNICAL_ARCHITECTURE.md)
2. Explore [WHY_CODEPULSE.md](WHY_CODEPULSE.md)
3. Check [CONTRIBUTING.md](CONTRIBUTING.md)
4. Run on your projects!

## Need Help?

- GitHub Issues: Report bugs
- Email: xsll7c@gmail.com
- Documentation: `/docs` folder

---

**Happy Analyzing! 🫀**
