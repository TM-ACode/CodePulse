# دليل الاستخدام - CodePulse v0.5.0

## 🚀 التثبيت السريع

### 1. فك الضغط
```bash
unzip CodePulse_v0.5.0_Final.zip
cd CodePulse
```

### 2. تثبيت المكتبات
```bash
# تثبيت networkx فقط (المكتبة الوحيدة المطلوبة)
pip install networkx

# أو تثبيت كل شي
pip install -e .
```

### 3. اختبار التثبيت
```bash
python3 -c "import networkx; print('✓ جاهز!')"
```

---

## 📊 المحللات الجديدة (8 محركات)

### 1️⃣ Deep Analysis Engine - التحليل العميق

**ماذا يفعل:**
- يبني Control Flow Graph (خريطة تنفيذ الكود)
- يبني Data Flow Graph (تتبع البيانات)
- يبني Call Graph (علاقات الدوال)
- يكتشف Unreachable code (كود لن ينفذ أبداً)
- يكتشف Infinite loops (حلقات لا نهائية)

**الاستخدام:**
```bash
python3 src/core/deep_analysis.py test_file.py
```

**النتيجة:**
```json
{
  "control_flow_analysis": {
    "issues": [
      {
        "type": "potential_infinite_loop",
        "severity": "error",
        "message": "Detected potential infinite loop"
      }
    ],
    "total_nodes": 228,
    "branch_points": 61,
    "cyclomatic_complexity": 6
  },
  "data_flow_analysis": {
    "issues": [
      {
        "type": "unused_variable",
        "variable": "x",
        "message": "Variable \"x\" defined but never used"
      }
    ]
  }
}
```

**مثال عملي:**
```bash
# اختبر على ملف TEST_EXAMPLE.py الموجود
python3 src/core/deep_analysis.py TEST_EXAMPLE.py
```

---

### 2️⃣ Clone Detection - كشف النسخ المكررة

**ماذا يفعل:**
يكتشف 4 أنواع من التكرار:
- **Type 1**: نسخ حرفي (copy-paste)
- **Type 2**: نفس الكود بأسماء متغيرات مختلفة
- **Type 3**: كود مشابه مع تعديلات
- **Type 4**: كود يعمل نفس الشيء بطريقة مختلفة (فريد!)

**الاستخدام:**
```bash
python3 src/core/clone_detection.py test_file.py
```

**النتيجة:**
```
CODE CLONE DETECTION REPORT
============================================================

Total Clones: 7
Duplicated Lines: 17

SEMANTIC CLONES (Type 4)
process_data_1 (line 56) ≈ process_data_2 (line 64)
Similarity: 75.0%
```

**مثال عملي:**
```bash
python3 src/core/clone_detection.py TEST_EXAMPLE.py
```

---

### 3️⃣ Smell Detector - كشف مشاكل الجودة

**ماذا يفعل:**
يكتشف 5 فئات من المشاكل:
- **Bloaters**: دوال طويلة، كلاسات كبيرة
- **OO Abusers**: مشاكل في OOP
- **Change Preventers**: كود صعب التعديل
- **Dispensables**: كود غير ضروري
- **Couplers**: ارتباط عالي بين الكلاسات

**الاستخدام:**
```bash
python3 src/core/smell_detector.py test_file.py
```

**النتيجة:**
```
INTELLIGENT CODE SMELL ANALYSIS
======================================================================

Code Health Score: 90.0/100
Total Smells: 2

[MEDIUM] Long Parameter List (Line 6)
  Impact: Hard to call, understand, and maintain.
  Fix: Use parameter objects or configuration classes.

[MEDIUM] Feature Envy (Line 77)
  Impact: Method is in the wrong class. Poor cohesion.
  Fix: Move this method to the 'other_obj' class.
```

**مثال عملي:**
```bash
python3 src/core/smell_detector.py TEST_EXAMPLE.py
```

---

### 4️⃣ Cross-File Analysis - تحليل البنية المعمارية

**ماذا يفعل:**
- يحلل الاعتماديات بين الملفات
- يكتشف Circular dependencies (اعتماديات دائرية)
- يحسب Module stability
- يكتشف God modules

**الاستخدام:**
```bash
python3 src/core/cross_file_analysis.py ./project_directory
```

**النتيجة:**
```
CROSS-FILE ARCHITECTURE ANALYSIS
======================================================================

Files Analyzed: 22
Architecture Score: 85.0/100

Issues Found: 2

[HIGH] Circular Dependency
  scanner.py → analyzer.py → scanner.py
  💡 Break cycle using dependency injection

[MEDIUM] God Module
  Module 'core' depends on 12 other modules
  💡 Split module into smaller components
```

**مثال عملي:**
```bash
python3 src/core/cross_file_analysis.py ./src/core
```

---

### 5️⃣ Quality Trends - تتبع الجودة عبر الزمن

**ماذا يفعل:**
- يحفظ نقاط قياس الجودة
- يحلل الاتجاه (تحسن / تدهور)
- يستخدم Linear Regression
- يحسب Volatility

**الاستخدام:**
```bash
# إضافة قياس جديد
python3 src/core/quality_trends.py add

# عرض الملخص
python3 src/core/quality_trends.py
```

**النتيجة:**
```json
{
  "current_score": 82.5,
  "best_score": 86.0,
  "trend": "improving",
  "slope": 0.8,
  "average_score": 79.2
}
```

---

### 6️⃣ Advanced Metrics - مقاييس متقدمة

**ماذا يحسب:**
- **Halstead Metrics** (Volume, Difficulty, Bugs)
- **Maintainability Index** (0-100)
- **Technical Debt** (بالساعات)
- **Cyclomatic Complexity**
- **Cognitive Complexity**

**الاستخدام:**
```python
from src.core.advanced_metrics import AdvancedMetricsCalculator

calc = AdvancedMetricsCalculator()
metrics = calc.calculate_file_metrics('test.py')
print(metrics['maintainability_index'])
```

---

### 7️⃣ Performance Analyzer - تحليل الأداء

**ماذا يكتشف:**
- حلقات متداخلة O(n²), O(n³)
- تسريبات الذاكرة
- عمليات غير فعالة
- String concatenation في حلقات

**الاستخدام:**
```python
from src.core.performance_analyzer import PerformanceAnalyzer

analyzer = PerformanceAnalyzer()
issues = analyzer.analyze_file('test.py')
```

---

### 8️⃣ Code Patterns - أنماط الكود

**ماذا يكتشف:**
- **Design Patterns**: Singleton, Factory, Builder
- **Anti-Patterns**: God Class, Spaghetti Code
- **Best Practices**: Docstrings, Type hints

**الاستخدام:**
```python
from src.core.code_patterns import PatternDetector

detector = PatternDetector()
patterns = detector.detect_patterns('test.py')
```

---

## 🎯 حالات الاستخدام العملية

### مثال 1: فحص ملف واحد

```bash
# 1. تحليل عميق
python3 src/core/deep_analysis.py myfile.py > analysis.json

# 2. كشف التكرار
python3 src/core/clone_detection.py myfile.py

# 3. كشف المشاكل
python3 src/core/smell_detector.py myfile.py
```

### مثال 2: فحص مشروع كامل

```bash
# 1. تحليل البنية المعمارية
python3 src/core/cross_file_analysis.py ./my_project

# 2. فحص كل الملفات
for file in $(find ./my_project -name "*.py"); do
    echo "=== $file ==="
    python3 src/core/smell_detector.py $file
done
```

### مثال 3: تتبع الجودة عبر الزمن

```bash
# قبل كل commit
python3 src/core/quality_trends.py add

# عرض التقدم
python3 src/core/quality_trends.py
```

---

## 📝 ملف الاختبار TEST_EXAMPLE.py

الملف يحتوي على:
✅ Long parameter list (7 parameters)
✅ Nested loops O(n²)
✅ Unused variables
✅ God class (UserManager)
✅ Nested if statements
✅ Duplicate code (process_data_1 vs process_data_2)
✅ Feature envy (Calculator.complex_calculation)
✅ Unreachable code
✅ Infinite loop

**جرب المحللات عليه:**
```bash
# تحليل عميق
python3 src/core/deep_analysis.py TEST_EXAMPLE.py | python3 -m json.tool

# كشف النسخ
python3 src/core/clone_detection.py TEST_EXAMPLE.py

# كشف المشاكل
python3 src/core/smell_detector.py TEST_EXAMPLE.py
```

---

## 🔧 نصائح الاستخدام

### 1. البداية
ابدأ بملف صغير أولاً:
```bash
python3 src/core/smell_detector.py small_file.py
```

### 2. التحليل العميق
استخدمه على الأجزاء المهمة فقط (أبطأ):
```bash
python3 src/core/deep_analysis.py critical_module.py
```

### 3. المشاريع الكبيرة
استخدم Cross-File Analysis:
```bash
python3 src/core/cross_file_analysis.py ./large_project
```

### 4. التتبع المستمر
أضف Quality Trends في CI/CD:
```bash
# في كل build
python3 src/core/quality_trends.py add
```

---

## ⚙️ التكوين

أنشئ ملف `codepulse.config.json`:

```json
{
  "clone_detection": {
    "min_lines": 6,
    "types": ["1", "2", "4"]
  },
  "smell_detection": {
    "max_method_length": 50,
    "max_parameters": 5,
    "max_complexity": 10
  },
  "excluded_dirs": [
    "tests",
    "venv",
    "__pycache__"
  ]
}
```

---

## 📊 فهم النتائج

### Control Flow Analysis
- **total_nodes**: عدد العمليات في الكود
- **branch_points**: نقاط القرار (if, for, etc.)
- **cyclomatic_complexity**: تعقيد المسارات

### Clone Detection
- **Type 1**: نسخ حرفي → احذفه
- **Type 2**: نفس الكود بأسماء مختلفة → استخرج دالة
- **Type 4**: نفس الوظيفة بطرق مختلفة → وحّدها

### Code Smells
- **HIGH**: أولوية عالية - اصلحه الآن
- **MEDIUM**: مهم - اصلحه قريباً
- **LOW**: تحسين - اصلحه لما تقدر

---

## 🐛 حل المشاكل

### مشكلة: ModuleNotFoundError
```bash
# تأكد من networkx
pip install networkx
```

### مشكلة: SyntaxError في الملف المراد فحصه
```
الملف يحتوي على أخطاء syntax - اصلحها أولاً
```

### مشكلة: بطء التحليل
```bash
# استخدم المحللات البسيطة أولاً
python3 src/core/smell_detector.py file.py  # سريع

# Deep analysis للملفات المهمة فقط
python3 src/core/deep_analysis.py critical.py  # أبطأ
```

---

## 📚 المزيد من المعلومات

- **QUICK_START.md** - ابدأ في 5 دقائق
- **TECHNICAL_ARCHITECTURE.md** - تفاصيل الخوارزميات
- **WHY_CODEPULSE.md** - لماذا مختلف
- **CONTRIBUTING.md** - كيف تساهم

---

## 💡 أمثلة متقدمة

### دمج في CI/CD

```yaml
# .github/workflows/code-quality.yml
- name: CodePulse Analysis
  run: |
    python3 src/core/cross_file_analysis.py ./src
    python3 src/core/quality_trends.py add
```

### سكريبت تلقائي

```bash
#!/bin/bash
# analyze.sh

echo "🫀 Running CodePulse Analysis..."

# Deep Analysis
python3 src/core/deep_analysis.py $1 > deep_analysis.json

# Clone Detection
python3 src/core/clone_detection.py $1 > clones.txt

# Smell Detection
python3 src/core/smell_detector.py $1 > smells.txt

echo "✅ Analysis complete!"
echo "Results: deep_analysis.json, clones.txt, smells.txt"
```

استخدام:
```bash
chmod +x analyze.sh
./analyze.sh myfile.py
```

---

**جرب الآن! 🚀**

```bash
cd CodePulse
python3 src/core/smell_detector.py TEST_EXAMPLE.py
```
