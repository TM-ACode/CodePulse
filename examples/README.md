# Examples Directory

This directory contains sample code files in different languages to demonstrate CodePulse's multi-language support.

## Sample Files

### Python
See the main `src/` directory for Python examples.

### JavaScript
- `sample.js` - Express.js application example
  - Demonstrates: classes, async/await, imports, exports
  - Intentional issues for testing

### TypeScript
- `sample.ts` - Type-safe code analyzer
  - Demonstrates: interfaces, types, generics, private methods
  - Shows TypeScript-specific features

## Testing CodePulse

You can test CodePulse on these examples:

```bash
# Scan all examples
python3 src/core/scanner.py ./examples

# Analyze JavaScript file
python3 src/core/js_scanner.py ./examples/sample.js

# Full comprehensive analysis
python3 src/core/analyzer.py ./examples
```

## What CodePulse Detects

### In JavaScript/TypeScript:
- ✅ Import/export statements
- ✅ Function declarations (regular, arrow, async)
- ✅ Class definitions
- ✅ Complexity calculations
- ✅ Security issues (hardcoded secrets, eval, etc.)
- ✅ Code structure

### In Python:
- ✅ AST-based analysis
- ✅ Full dependency graph
- ✅ Function/class extraction
- ✅ Docstrings and type hints
- ✅ Security vulnerabilities
- ✅ Detailed metrics

## Add Your Own Examples

Feel free to add more example files in different languages to test CodePulse's capabilities!

Supported languages:
- Python (.py)
- JavaScript (.js, .jsx)
- TypeScript (.ts, .tsx)
- Java (.java)
- C/C++ (.c, .cpp, .h)
- Go (.go)
- Rust (.rs)
- And more...

---

**Note**: These examples contain intentional code issues for testing purposes!
