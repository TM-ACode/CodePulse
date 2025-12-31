#!/usr/bin/env python3
"""
CodePulse Demo Script
========================

Quick demo of what CodePulse can do. I built this to show off the features!

Run with: python demo.py

Author: Saleh Almqati
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from core.scanner import PulseScanner
from core.ai_engine import AIEngine
from modules.security import SecurityScanner

console = Console()


def print_banner():
    """Print a nice banner"""
    banner = """
    ╔═══════════════════════════════════════════════════════╗
    ║                                                       ║
    ║         🛡️  CodePulse Demo                        ║
    ║         Built by Saleh Almqati                       ║
    ║         A Student Project for Code Quality           ║
    ║                                                       ║
    ╚═══════════════════════════════════════════════════════╝
    """
    console.print(banner, style="bold cyan")


def demo_scanner():
    """Demonstrate the scanner functionality"""
    console.print("\n[bold yellow]1. Project Scanner Demo[/bold yellow]")
    console.print("[dim]Scanning the CodePulse project itself...[/dim]\n")
    
    try:
        scanner = PulseScanner("./src")
        structure = scanner.scan()
        
        # Create results table
        table = Table(title="📊 Scan Results", show_header=True)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Total Files", str(structure.total_files))
        table.add_row("Total Lines", f"{structure.total_lines:,}")
        table.add_row("Python Files", str(structure.languages.get('Python', 0)))
        table.add_row("Dependencies Found", str(len(structure.dependency_graph)))
        
        console.print(table)
        
        # Show some file details
        if structure.files:
            console.print("\n[bold]Sample Files:[/bold]")
            for file_meta in structure.files[:3]:
                console.print(f"  • {file_meta.path} - {file_meta.lines} lines")
        
        return True
    except Exception as e:
        console.print(f"[red]Error in scanner demo: {e}[/red]")
        return False


def demo_ai_analysis():
    """Demonstrate AI analysis"""
    console.print("\n[bold yellow]2. AI Analysis Demo[/bold yellow]")
    console.print("[dim]Analyzing code with AI (using mock mode)...[/dim]\n")
    
    try:
        # Sample code to analyze
        sample_code = '''
def process_data(items):
    """Process a list of items"""
    result = []
    for item in items:
        for i in range(len(items)):
            if items[i]['id'] == item['id']:
                result.append(items[i])
    return result

def get_user(user_id):
    query = f"SELECT * FROM users WHERE id={user_id}"
    return execute_query(query)
'''
        
        engine = AIEngine()  # Will use mock mode without API key
        result = engine.analyze_code(
            code=sample_code,
            file_path="example.py",
            context={'imports': [], 'functions': ['process_data', 'get_user'], 'complexity': 12}
        )
        
        # Display results
        console.print(f"[bold]Overall Score:[/bold] {result.overall_score}/100\n")
        
        if result.issues:
            console.print("[bold]Issues Found:[/bold]")
            for issue in result.issues[:3]:  # Show first 3
                severity_color = {
                    'critical': 'red',
                    'high': 'orange1',
                    'medium': 'yellow',
                    'low': 'cyan'
                }.get(issue.severity.value, 'white')
                
                console.print(f"  • [{severity_color}]{issue.title}[/{severity_color}]")
                console.print(f"    Line {issue.line_number} | {issue.description[:80]}...")
        
        if result.suggestions:
            console.print("\n[bold]Suggestions:[/bold]")
            for suggestion in result.suggestions[:2]:
                console.print(f"  💡 {suggestion}")
        
        return True
    except Exception as e:
        console.print(f"[red]Error in AI demo: {e}[/red]")
        import traceback
        traceback.print_exc()
        return False


def demo_security_scanner():
    """Demonstrate security scanning"""
    console.print("\n[bold yellow]3. Security Scanner Demo[/bold yellow]")
    console.print("[dim]Scanning for security vulnerabilities...[/dim]\n")
    
    try:
        # Create a temporary file with vulnerabilities
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('''
# Sample code with vulnerabilities
import os

# Hardcoded credentials
API_KEY = "sk-1234567890abcdefghijklmnop"
PASSWORD = "super_secret_password_123"

def get_user(user_id):
    # SQL injection vulnerability
    query = f"SELECT * FROM users WHERE id={user_id}"
    return execute_query(query)

def run_command(cmd):
    # Command injection vulnerability
    os.system("ls " + cmd)

# Weak crypto
import hashlib
hash = hashlib.md5(b"password").hexdigest()
''')
            temp_file = f.name
        
        try:
            scanner = SecurityScanner()
            issues = scanner.scan_file(temp_file)
            report = scanner.generate_report(issues)
            
            # Display results
            score = report['security_score']
            score_color = 'green' if score >= 80 else 'yellow' if score >= 60 else 'red'
            
            console.print(f"[bold]Security Score:[/bold] [{score_color}]{score}/100[/{score_color}]\n")
            
            # Issues breakdown
            table = Table(title="🚨 Security Issues")
            table.add_column("Severity", style="cyan")
            table.add_column("Count", style="yellow")
            
            for severity, count in report['severity_breakdown'].items():
                if count > 0:
                    table.add_row(severity.upper(), str(count))
            
            console.print(table)
            
            # Show sample issues
            if issues:
                console.print("\n[bold red]Sample Issues:[/bold red]")
                for issue in issues[:3]:
                    console.print(f"  • {issue.title}")
                    console.print(f"    {issue.description[:80]}...")
        
        finally:
            os.unlink(temp_file)
        
        return True
    except Exception as e:
        console.print(f"[red]Error in security demo: {e}[/red]")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all demos"""
    print_banner()
    
    console.print("\n[bold cyan]Welcome to the CodePulse Demo![/bold cyan]")
    console.print("This demo will showcase the three main features:\n")
    
    results = []
    
    # Run demos
    results.append(("Scanner", demo_scanner()))
    results.append(("AI Analysis", demo_ai_analysis()))
    results.append(("Security Scan", demo_security_scanner()))
    
    # Summary
    console.print("\n" + "="*60)
    console.print("[bold cyan]Demo Summary[/bold cyan]\n")
    
    for name, success in results:
        status = "[green]✓[/green]" if success else "[red]✗[/red]"
        console.print(f"{status} {name}")
    
    console.print("\n" + "="*60)
    console.print("\n[bold green]Demo complete! 🎉[/bold green]")
    console.print("\nNext steps:")
    console.print("  1. Read the [cyan]README.md[/cyan] for full documentation")
    console.print("  2. Try: [yellow]pulse scan .[/yellow] to scan a project")
    console.print("  3. Check out [cyan]docs/QUICKSTART.md[/cyan] for more examples")
    console.print("\nFor AI features, set your API key:")
    console.print("  [yellow]export ANTHROPIC_API_KEY='your-key'[/yellow]\n")


if __name__ == '__main__':
    main()
