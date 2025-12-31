"""
Comprehensive Code Scanner
===========================

Runs ALL analysis engines in one command:
1. Deep Analysis (CFG, DFG, Call Graphs)
2. Clone Detection (4 types)
3. Code Smells (5 categories)
4. Advanced Security (OWASP Top 10)
5. Performance Analysis
6. Code Metrics
7. Best Practices

Usage:
    python comprehensive_scan.py <file_or_directory>
"""

import os
import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

# Import all analysis engines
try:
    from deep_analysis_standalone import DeepAnalysisEngine
except:
    from src.core.deep_analysis_standalone import DeepAnalysisEngine

try:
    from clone_detection import CloneDetector, SemanticCloneDetector
except:
    from src.core.clone_detection import CloneDetector, SemanticCloneDetector

try:
    from smell_detector import IntelligentSmellDetector
except:
    from src.core.smell_detector import IntelligentSmellDetector

try:
    from advanced_security import AdvancedSecurityScanner
except:
    from src.core.advanced_security import AdvancedSecurityScanner

try:
    from performance_analyzer import PerformanceAnalyzer
except:
    try:
        from src.core.performance_analyzer import PerformanceAnalyzer
    except:
        PerformanceAnalyzer = None

try:
    from advanced_metrics import AdvancedMetricsCalculator
except:
    try:
        from src.core.advanced_metrics import AdvancedMetricsCalculator
    except:
        AdvancedMetricsCalculator = None


class ComprehensiveScanner:
    """
    Runs all analysis engines and generates unified report.
    """
    
    def __init__(self):
        self.results = {}
        self.start_time = None
        self.end_time = None
        
    def scan_file(self, file_path: str) -> Dict[str, Any]:
        """Comprehensive scan of single file"""
        print(f"\n{'='*70}")
        print(f"🫀 CODEPULSE - COMPREHENSIVE ANALYSIS")
        print(f"{'='*70}")
        print(f"\nFile: {file_path}")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        self.start_time = time.time()
        
        # 1. Deep Analysis
        print("⚙️  Running Deep Analysis...")
        deep_engine = DeepAnalysisEngine()
        deep_results = deep_engine.analyze_file(file_path)
        self.results['deep_analysis'] = deep_results
        print("   ✓ Complete")
        
        # 2. Clone Detection
        print("⚙️  Running Clone Detection...")
        clone_detector = CloneDetector(min_lines=6)
        clones = clone_detector.detect_clones_in_file(file_path)
        clone_report = clone_detector.get_clone_report()
        self.results['clone_detection'] = clone_report
        print(f"   ✓ Found {clone_report['total_clones']} clones")
        
        # 3. Code Smells
        print("⚙️  Running Smell Detection...")
        smell_detector = IntelligentSmellDetector()
        smells = smell_detector.detect_smells(file_path)
        smell_report = smell_detector.get_smell_report()
        self.results['code_smells'] = smell_report
        print(f"   ✓ Found {smell_report['total_smells']} smells")
        
        # 4. Security Scan
        print("⚙️  Running Security Scan...")
        security_scanner = AdvancedSecurityScanner()
        security_issues = security_scanner.scan_file(file_path)
        security_report = security_scanner.get_report()
        self.results['security'] = security_report
        print(f"   ✓ Found {security_report['total_issues']} security issues")
        
        # 5. Performance Analysis
        if PerformanceAnalyzer:
            print("⚙️  Running Performance Analysis...")
            try:
                perf_analyzer = PerformanceAnalyzer()
                perf_issues = perf_analyzer.analyze_file(file_path)
                self.results['performance'] = {
                    'total_issues': len(perf_issues),
                    'issues': perf_issues
                }
                print(f"   ✓ Found {len(perf_issues)} performance issues")
            except:
                print("   ⚠ Performance analysis skipped")
        
        # 6. Advanced Metrics
        if AdvancedMetricsCalculator:
            print("⚙️  Calculating Advanced Metrics...")
            try:
                metrics_calc = AdvancedMetricsCalculator()
                metrics = metrics_calc.calculate_file_metrics(file_path)
                self.results['metrics'] = metrics
                print("   ✓ Metrics calculated")
            except:
                print("   ⚠ Metrics calculation skipped")
        
        self.end_time = time.time()
        
        # Calculate overall score
        self.results['overall_score'] = self._calculate_overall_score()
        self.results['scan_time'] = round(self.end_time - self.start_time, 2)
        
        return self.results
    
    def scan_directory(self, dir_path: str) -> Dict[str, Any]:
        """Scan all Python files in directory"""
        print(f"\n{'='*70}")
        print(f"🫀 CODEPULSE - PROJECT SCAN")
        print(f"{'='*70}")
        print(f"\nDirectory: {dir_path}")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Find all Python files
        python_files = []
        for root, dirs, files in os.walk(dir_path):
            # Skip common directories
            dirs[:] = [d for d in dirs if d not in ['__pycache__', 'venv', '.git', 'node_modules']]
            
            for file in files:
                if file.endswith('.py'):
                    python_files.append(os.path.join(root, file))
        
        print(f"Found {len(python_files)} Python files\n")
        
        # Scan each file
        all_results = {}
        total_issues = {
            'security': 0,
            'smells': 0,
            'clones': 0,
            'performance': 0
        }
        
        for i, file_path in enumerate(python_files, 1):
            print(f"[{i}/{len(python_files)}] {os.path.basename(file_path)}")
            
            try:
                result = self.scan_file(file_path)
                all_results[file_path] = result
                
                # Aggregate
                total_issues['security'] += result.get('security', {}).get('total_issues', 0)
                total_issues['smells'] += result.get('code_smells', {}).get('total_smells', 0)
                total_issues['clones'] += result.get('clone_detection', {}).get('total_clones', 0)
                total_issues['performance'] += result.get('performance', {}).get('total_issues', 0)
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
                continue
        
        # Project summary
        project_summary = {
            'total_files': len(python_files),
            'files_scanned': len(all_results),
            'total_issues': total_issues,
            'project_score': self._calculate_project_score(all_results),
            'files': all_results
        }
        
        return project_summary
    
    def _calculate_overall_score(self) -> float:
        """Calculate overall code quality score"""
        weights = {
            'security': 0.35,
            'code_smells': 0.25,
            'deep_analysis': 0.20,
            'clones': 0.10,
            'performance': 0.10
        }
        
        scores = {}
        
        # Security score
        if 'security' in self.results:
            scores['security'] = self.results['security'].get('security_score', 0)
        
        # Smell score
        if 'code_smells' in self.results:
            scores['code_smells'] = self.results['code_smells'].get('code_health_score', 0)
        
        # Deep analysis score
        if 'deep_analysis' in self.results:
            scores['deep_analysis'] = self.results['deep_analysis'].get('code_quality_score', 0)
        
        # Clone score (inverse of duplication)
        if 'clone_detection' in self.results:
            clones = self.results['clone_detection'].get('total_clones', 0)
            scores['clones'] = max(0, 100 - (clones * 5))
        
        # Performance score
        if 'performance' in self.results:
            perf_issues = self.results['performance'].get('total_issues', 0)
            scores['performance'] = max(0, 100 - (perf_issues * 10))
        
        # Weighted average
        total_score = 0
        total_weight = 0
        for key, weight in weights.items():
            if key in scores:
                total_score += scores[key] * weight
                total_weight += weight
        
        return round(total_score / total_weight if total_weight > 0 else 0, 1)
    
    def _calculate_project_score(self, all_results: Dict) -> float:
        """Calculate project-wide score"""
        if not all_results:
            return 0.0
        
        scores = [r.get('overall_score', 0) for r in all_results.values()]
        return round(sum(scores) / len(scores), 1)
    
    def print_summary(self):
        """Print beautiful summary report"""
        print(f"\n{'='*70}")
        print("📊 COMPREHENSIVE ANALYSIS RESULTS")
        print(f"{'='*70}\n")
        
        # Overall Score
        score = self.results.get('overall_score', 0)
        grade = self._get_grade(score)
        print(f"Overall Score: {score}/100 ({grade})")
        print(f"Scan Time: {self.results.get('scan_time', 0)}s\n")
        
        # Deep Analysis
        if 'deep_analysis' in self.results:
            deep = self.results['deep_analysis']
            print(f"{'─'*70}")
            print("🧠 DEEP ANALYSIS")
            print(f"{'─'*70}")
            
            cf = deep.get('control_flow_analysis', {})
            print(f"Control Flow:")
            print(f"  • Nodes: {cf.get('total_nodes', 0)}")
            print(f"  • Edges: {cf.get('total_edges', 0)}")
            print(f"  • Branch Points: {cf.get('branch_points', 0)}")
            print(f"  • Complexity: {cf.get('cyclomatic_complexity', 0)}")
            
            if cf.get('issues'):
                print(f"  Issues:")
                for issue in cf['issues']:
                    print(f"    ⚠  {issue['message']}")
            
            df = deep.get('data_flow_analysis', {})
            print(f"\nData Flow:")
            print(f"  • Variables: {df.get('total_variables', 0)}")
            print(f"  • Dependencies: {df.get('data_dependencies', 0)}")
            
            if df.get('issues'):
                for issue in df['issues'][:3]:
                    print(f"    ⚠  {issue['message']}")
            print()
        
        # Security
        if 'security' in self.results:
            sec = self.results['security']
            print(f"{'─'*70}")
            print("🔒 SECURITY ANALYSIS")
            print(f"{'─'*70}")
            print(f"Security Score: {sec.get('security_score', 0)}/100")
            print(f"Total Issues: {sec.get('total_issues', 0)}\n")
            
            by_sev = sec.get('by_severity', {})
            if any(by_sev.values()):
                print("By Severity:")
                for sev in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
                    count = by_sev.get(sev, 0)
                    if count > 0:
                        icon = '🔴' if sev == 'CRITICAL' else '🟠' if sev == 'HIGH' else '🟡' if sev == 'MEDIUM' else '🟢'
                        print(f"  {icon} {sev}: {count}")
            
            if sec.get('issues'):
                print(f"\nTop Security Issues:")
                for issue in sec['issues'][:3]:
                    print(f"  [{issue['severity']}] {issue['type']}")
                    print(f"    Line {issue['line']}: {issue['description']}")
                    print(f"    💡 {issue['recommendation']}")
            print()
        
        # Code Smells
        if 'code_smells' in self.results:
            smells = self.results['code_smells']
            print(f"{'─'*70}")
            print("👃 CODE SMELLS")
            print(f"{'─'*70}")
            print(f"Health Score: {smells.get('code_health_score', 0)}/100")
            print(f"Total Smells: {smells.get('total_smells', 0)}\n")
            
            by_cat = smells.get('by_category', {})
            if by_cat:
                print("By Category:")
                for cat, count in by_cat.items():
                    print(f"  • {cat}: {count}")
            
            if smells.get('smells'):
                print(f"\nTop Smells:")
                for smell in smells['smells'][:3]:
                    print(f"  [{smell['severity']}] {smell['name']} (Line {smell['line']})")
                    print(f"    💡 {smell['refactoring']}")
            print()
        
        # Clone Detection
        if 'clone_detection' in self.results:
            clones = self.results['clone_detection']
            print(f"{'─'*70}")
            print("🔍 CLONE DETECTION")
            print(f"{'─'*70}")
            print(f"Total Clones: {clones.get('total_clones', 0)}")
            print(f"Duplicated Lines: {clones.get('total_duplicated_lines', 0)}\n")
            
            by_type = clones.get('clones_by_type', {})
            if by_type:
                print("By Type:")
                for type_name, count in by_type.items():
                    print(f"  • {type_name}: {count}")
            print()
        
        # Recommendations
        print(f"{'─'*70}")
        print("🎯 PRIORITY RECOMMENDATIONS")
        print(f"{'─'*70}")
        
        recs = self._generate_recommendations()
        for i, rec in enumerate(recs[:5], 1):
            print(f"{i}. {rec}")
        
        print(f"\n{'='*70}\n")
    
    def _get_grade(self, score: float) -> str:
        """Get letter grade"""
        if score >= 90:
            return "A+"
        elif score >= 85:
            return "A"
        elif score >= 80:
            return "B+"
        elif score >= 75:
            return "B"
        elif score >= 70:
            return "C+"
        elif score >= 60:
            return "C"
        else:
            return "D"
    
    def _generate_recommendations(self) -> List[str]:
        """Generate priority recommendations"""
        recs = []
        
        # Security
        if 'security' in self.results:
            sec = self.results['security']
            if sec.get('by_severity', {}).get('CRITICAL', 0) > 0:
                recs.append("⚡ URGENT: Fix CRITICAL security vulnerabilities")
            if sec.get('by_severity', {}).get('HIGH', 0) > 0:
                recs.append("🔴 HIGH: Address high-severity security issues")
        
        # Code Smells
        if 'code_smells' in self.results:
            smells = self.results['code_smells']
            if smells.get('total_smells', 0) > 10:
                recs.append("🟡 MEDIUM: Refactor code smells for better maintainability")
        
        # Clones
        if 'clone_detection' in self.results:
            clones = self.results['clone_detection']
            if clones.get('total_duplicated_lines', 0) > 50:
                recs.append("🟡 MEDIUM: Reduce code duplication")
        
        # Performance
        if 'performance' in self.results:
            perf = self.results['performance']
            if perf.get('total_issues', 0) > 5:
                recs.append("🟢 LOW: Optimize performance bottlenecks")
        
        if not recs:
            recs.append("✅ Great! No major issues found.")
        
        return recs
    
    def save_report(self, output_path: str):
        """Save detailed JSON report"""
        with open(output_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"💾 Report saved to: {output_path}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python comprehensive_scan.py <file_or_directory>")
        sys.exit(1)
    
    target = sys.argv[1]
    scanner = ComprehensiveScanner()
    
    if os.path.isfile(target):
        results = scanner.scan_file(target)
        scanner.print_summary()
        
        # Save report
        report_path = f"comprehensive_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        scanner.save_report(report_path)
        
    elif os.path.isdir(target):
        results = scanner.scan_directory(target)
        
        print(f"\n{'='*70}")
        print("📊 PROJECT SUMMARY")
        print(f"{'='*70}\n")
        print(f"Total Files: {results['total_files']}")
        print(f"Files Scanned: {results['files_scanned']}")
        print(f"Project Score: {results['project_score']}/100\n")
        
        print("Total Issues:")
        for issue_type, count in results['total_issues'].items():
            print(f"  • {issue_type.title()}: {count}")
        
        # Save report
        report_path = f"project_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_path, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n💾 Report saved to: {report_path}")
        
    else:
        print(f"Error: {target} is not a file or directory")
        sys.exit(1)


if __name__ == '__main__':
    main()
