#!/usr/bin/env python3
"""
Reports Manager
===============

Simple utility to manage CodePulse reports.

Author: Saleh Almqati
"""

import os
import json
import glob
from datetime import datetime
from pathlib import Path


class ReportsManager:
    """Manage analysis reports"""
    
    def __init__(self, reports_dir: str = "reports"):
        """
        Initialize reports manager.
        
        Args:
            reports_dir: Directory where reports are stored
        """
        self.reports_dir = Path(reports_dir)
        self.reports_dir.mkdir(exist_ok=True)
    
    def list_reports(self) -> list:
        """
        List all reports in the reports directory.
        
        Returns:
            List of report file paths
        """
        pattern = str(self.reports_dir / "comprehensive_report_*.json")
        reports = sorted(glob.glob(pattern), reverse=True)
        return reports
    
    def get_latest_report(self) -> str:
        """
        Get the most recent report.
        
        Returns:
            Path to latest report or None
        """
        reports = self.list_reports()
        return reports[0] if reports else None
    
    def load_report(self, report_path: str) -> dict:
        """
        Load a report from file.
        
        Args:
            report_path: Path to report file
            
        Returns:
            Report data as dictionary
        """
        with open(report_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def print_summary(self, report_path: str):
        """
        Print a quick summary of a report.
        
        Args:
            report_path: Path to report file
        """
        report = self.load_report(report_path)
        
        filename = os.path.basename(report_path)
        print(f"\n{'='*60}")
        print(f"Report: {filename}")
        print(f"{'='*60}")
        print(f"Project: {report['project_path']}")
        print(f"Date: {report['scan_date']}")
        print(f"Score: {report['overall_score']:.1f}/100 - {report['grade']}")
        print(f"Files: {report['total_files']} | Lines: {report['total_lines']:,}")
        print(f"Issues: {report['total_issues']} | Security: {report['security_issues']}")
        print(f"{'='*60}\n")
    
    def compare_reports(self, report1_path: str, report2_path: str):
        """
        Compare two reports and show improvements/regressions.
        
        Args:
            report1_path: Path to first (older) report
            report2_path: Path to second (newer) report
        """
        report1 = self.load_report(report1_path)
        report2 = self.load_report(report2_path)
        
        print("\n" + "="*60)
        print("REPORT COMPARISON")
        print("="*60)
        
        print(f"\nOLD: {os.path.basename(report1_path)}")
        print(f"NEW: {os.path.basename(report2_path)}")
        
        print(f"\n{'Metric':<30} {'Old':<15} {'New':<15} {'Change'}")
        print("-"*60)
        
        # Compare scores
        metrics = [
            ('Overall Score', 'overall_score'),
            ('Code Quality', 'avg_quality_score'),
            ('Security Score', 'security_score'),
            ('Total Issues', 'total_issues'),
            ('Security Issues', 'security_issues'),
            ('Critical Issues', 'critical_issues'),
        ]
        
        for name, key in metrics:
            old_val = report1.get(key, 0)
            new_val = report2.get(key, 0)
            diff = new_val - old_val
            
            # Determine if change is good or bad
            if key in ['total_issues', 'security_issues', 'critical_issues']:
                # Lower is better for issues
                symbol = "✓" if diff <= 0 else "✗"
                color = "improved" if diff <= 0 else "regressed"
            else:
                # Higher is better for scores
                symbol = "✓" if diff >= 0 else "✗"
                color = "improved" if diff >= 0 else "regressed"
            
            change_str = f"{symbol} {diff:+.1f}" if isinstance(diff, float) else f"{symbol} {diff:+d}"
            print(f"{name:<30} {old_val:<15.1f} {new_val:<15.1f} {change_str}")
        
        print("\n" + "="*60 + "\n")
    
    def delete_report(self, report_path: str):
        """
        Delete a report file.
        
        Args:
            report_path: Path to report to delete
        """
        if os.path.exists(report_path):
            os.remove(report_path)
            print(f"Deleted: {report_path}")
        else:
            print(f"Report not found: {report_path}")
    
    def delete_old_reports(self, keep_last: int = 5):
        """
        Delete old reports, keeping only the most recent ones.
        
        Args:
            keep_last: Number of recent reports to keep
        """
        reports = self.list_reports()
        
        if len(reports) <= keep_last:
            print(f"Only {len(reports)} reports found, nothing to delete.")
            return
        
        to_delete = reports[keep_last:]
        print(f"\nDeleting {len(to_delete)} old reports (keeping {keep_last} most recent):")
        
        for report_path in to_delete:
            filename = os.path.basename(report_path)
            os.remove(report_path)
            print(f"  ✓ Deleted: {filename}")
        
        print(f"\nCleaned up! {len(to_delete)} reports deleted.\n")
    
    def export_summary_csv(self, output_file: str = "reports_summary.csv"):
        """
        Export a CSV summary of all reports.
        
        Args:
            output_file: Output CSV file path
        """
        reports = self.list_reports()
        
        if not reports:
            print("No reports found.")
            return
        
        import csv
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow([
                'Date', 'Project', 'Overall Score', 'Grade',
                'Code Quality', 'Security Score',
                'Total Issues', 'Security Issues',
                'Files', 'Lines'
            ])
            
            # Data
            for report_path in reports:
                report = self.load_report(report_path)
                writer.writerow([
                    report['scan_date'],
                    report['project_path'],
                    report['overall_score'],
                    report['grade'],
                    report['avg_quality_score'],
                    report['security_score'],
                    report['total_issues'],
                    report['security_issues'],
                    report['total_files'],
                    report['total_lines']
                ])
        
        print(f"\nSummary exported to: {output_file}\n")


def main():
    """CLI for reports manager"""
    import sys
    
    manager = ReportsManager()
    
    if len(sys.argv) < 2:
        print("Reports Manager - Manage CodePulse analysis reports")
        print("\nUsage:")
        print("  python reports_manager.py list              # List all reports")
        print("  python reports_manager.py latest            # Show latest report")
        print("  python reports_manager.py compare <n1> <n2> # Compare two reports")
        print("  python reports_manager.py delete <n>        # Delete a specific report")
        print("  python reports_manager.py clean [keep]      # Delete old reports (keep last N)")
        print("  python reports_manager.py export            # Export summary to CSV")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "list":
        reports = manager.list_reports()
        if not reports:
            print("No reports found in reports/ directory.")
        else:
            print(f"\nFound {len(reports)} reports:\n")
            for i, report_path in enumerate(reports, 1):
                manager.print_summary(report_path)
    
    elif command == "latest":
        latest = manager.get_latest_report()
        if latest:
            manager.print_summary(latest)
            print(f"Full report: {latest}")
        else:
            print("No reports found.")
    
    elif command == "compare":
        if len(sys.argv) < 4:
            print("Usage: python reports_manager.py compare <report1> <report2>")
            sys.exit(1)
        
        report1 = sys.argv[2]
        report2 = sys.argv[3]
        
        if not os.path.exists(report1) or not os.path.exists(report2):
            print("Error: One or both report files not found.")
            sys.exit(1)
        
        manager.compare_reports(report1, report2)
    
    elif command == "delete":
        if len(sys.argv) < 3:
            print("Usage: python reports_manager.py delete <report_path>")
            sys.exit(1)
        
        report_path = sys.argv[2]
        manager.delete_report(report_path)
    
    elif command == "clean":
        keep_last = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        manager.delete_old_reports(keep_last=keep_last)
    
    elif command == "export":
        manager.export_summary_csv()
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == '__main__':
    main()
