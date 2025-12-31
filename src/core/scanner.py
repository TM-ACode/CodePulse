"""
CodePulse Scanner Module
============================

Multi-language project scanning with support for Python, JavaScript, TypeScript, and more.

Analyzes project structure, extracts functions, classes, dependencies,
and builds a comprehensive dependency graph.

Author: Saleh Almqati
License: MIT
"""

import ast
import os
import pathlib
import json
from typing import Dict, List, Set, Optional, Any
from dataclasses import dataclass, field, asdict
from collections import defaultdict
import hashlib
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Language extensions mapping
LANGUAGE_EXTENSIONS = {
    'Python': ['.py', '.pyw'],
    'JavaScript': ['.js', '.jsx', '.mjs'],
    'TypeScript': ['.ts', '.tsx'],
    'Java': ['.java'],
    'C++': ['.cpp', '.cc', '.cxx', '.hpp', '.h'],
    'C': ['.c', '.h'],
    'Go': ['.go'],
    'Rust': ['.rs'],
    'Ruby': ['.rb'],
    'PHP': ['.php'],
    'Swift': ['.swift'],
    'Kotlin': ['.kt', '.kts'],
    'HTML': ['.html', '.htm'],
    'CSS': ['.css', '.scss', '.sass', '.less'],
    'JSON': ['.json'],
    'YAML': ['.yml', '.yaml'],
    'XML': ['.xml'],
    'Markdown': ['.md'],
    'Shell': ['.sh', '.bash'],
    'SQL': ['.sql'],
}


@dataclass
class FileMetadata:
    """Metadata for a scanned file"""
    path: str
    size: int
    lines: int
    language: str
    file_hash: str
    imports: List[str] = field(default_factory=list)
    functions: List[Dict[str, Any]] = field(default_factory=list)
    classes: List[Dict[str, Any]] = field(default_factory=list)
    complexity_score: float = 0.0
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)


@dataclass
class ProjectStructure:
    """Complete project structure representation"""
    root_path: str
    total_files: int = 0
    total_lines: int = 0
    languages: Dict[str, int] = field(default_factory=dict)
    files: List[FileMetadata] = field(default_factory=list)
    dependency_graph: Dict[str, List[str]] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'root_path': self.root_path,
            'total_files': self.total_files,
            'total_lines': self.total_lines,
            'languages': self.languages,
            'files': [f.to_dict() for f in self.files],
            'dependency_graph': self.dependency_graph
        }


class PulseScanner:
    """
    Advanced project scanner with AST-based analysis capabilities.
    
    This scanner goes beyond simple file reading by:
    - Using Abstract Syntax Trees to understand code structure
    - Building dependency graphs between modules
    - Calculating complexity metrics
    - Identifying code patterns and anti-patterns
    """
    
    # Files and directories to exclude from scanning
    EXCLUDE_PATTERNS = {
        '__pycache__', '.git', '.svn', '.hg', 'node_modules',
        '.venv', 'venv', 'env', '.idea', '.vscode', 'dist',
        'build', '*.pyc', '*.pyo', '*.egg-info', '.DS_Store'
    }
    
    # Supported file extensions and their languages
    LANGUAGE_MAP = {
        # Python
        '.py': 'Python',
        '.pyw': 'Python',
        # JavaScript
        '.js': 'JavaScript',
        '.jsx': 'JavaScript',
        '.mjs': 'JavaScript',
        # TypeScript
        '.ts': 'TypeScript',
        '.tsx': 'TypeScript',
        # Java
        '.java': 'Java',
        # C/C++
        '.cpp': 'C++',
        '.cc': 'C++',
        '.cxx': 'C++',
        '.hpp': 'C++',
        '.h': 'C/C++',
        '.c': 'C',
        # Go
        '.go': 'Go',
        # Rust
        '.rs': 'Rust',
        # Ruby
        '.rb': 'Ruby',
        # PHP
        '.php': 'PHP',
        # Swift
        '.swift': 'Swift',
        # Kotlin
        '.kt': 'Kotlin',
        '.kts': 'Kotlin',
        # Web
        '.html': 'HTML',
        '.htm': 'HTML',
        '.css': 'CSS',
        '.scss': 'CSS',
        '.sass': 'CSS',
        # Data
        '.json': 'JSON',
        '.xml': 'XML',
        '.yml': 'YAML',
        '.yaml': 'YAML',
        # Other
        '.md': 'Markdown',
        '.sh': 'Shell',
        '.bash': 'Shell',
        '.sql': 'SQL',
    }
    
    def __init__(self, root_path: str, max_depth: int = 10, follow_symlinks: bool = False):
        """
        Initialize the scanner.
        
        Args:
            root_path: Root directory to scan
            max_depth: Maximum directory depth to traverse
            follow_symlinks: Whether to follow symbolic links
        """
        self.root_path = pathlib.Path(root_path).resolve()
        self.max_depth = max_depth
        self.follow_symlinks = follow_symlinks
        self.structure = ProjectStructure(root_path=str(self.root_path))
        
        logger.info(f"Initialized scanner for: {self.root_path}")
    
    def should_exclude(self, path: pathlib.Path) -> bool:
        """
        Determine if a path should be excluded from scanning.
        
        Args:
            path: Path to check
            
        Returns:
            True if path should be excluded
        """
        for pattern in self.EXCLUDE_PATTERNS:
            if pattern.startswith('*'):
                # Wildcard pattern
                if path.name.endswith(pattern[1:]):
                    return True
            else:
                # Direct match
                if pattern in path.parts:
                    return True
        return False
    
    def calculate_file_hash(self, file_path: pathlib.Path) -> str:
        """
        Calculate SHA-256 hash of a file for integrity verification.
        
        Args:
            file_path: Path to file
            
        Returns:
            Hex digest of file hash
        """
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                # Read in chunks for memory efficiency
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception as e:
            logger.warning(f"Could not hash file {file_path}: {e}")
            return ""
    
    def analyze_python_ast(self, file_path: pathlib.Path) -> Dict[str, Any]:
        """
        Perform deep AST analysis on Python files.
        
        This method extracts:
        - Import statements and dependencies
        - Function definitions with parameters and docstrings
        - Class definitions with methods
        - Cyclomatic complexity estimates
        
        Args:
            file_path: Path to Python file
            
        Returns:
            Dictionary containing analysis results
        """
        result = {
            'imports': [],
            'functions': [],
            'classes': [],
            'complexity': 0
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            # Parse the source code into an AST
            tree = ast.parse(source_code, filename=str(file_path))
            
            # Walk through the AST
            for node in ast.walk(tree):
                # Extract imports
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        result['imports'].append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        result['imports'].append(node.module)
                
                # Extract function definitions
                elif isinstance(node, ast.FunctionDef):
                    func_info = {
                        'name': node.name,
                        'args': [arg.arg for arg in node.args.args],
                        'lineno': node.lineno,
                        'docstring': ast.get_docstring(node),
                        'is_async': isinstance(node, ast.AsyncFunctionDef)
                    }
                    result['functions'].append(func_info)
                    
                    # Simple complexity estimation (count decision points)
                    result['complexity'] += sum(1 for _ in ast.walk(node) 
                                               if isinstance(_, (ast.If, ast.For, ast.While, 
                                                               ast.ExceptHandler, ast.With)))
                
                # Extract class definitions
                elif isinstance(node, ast.ClassDef):
                    class_info = {
                        'name': node.name,
                        'lineno': node.lineno,
                        'docstring': ast.get_docstring(node),
                        'methods': [],
                        'bases': [base.id for base in node.bases if isinstance(base, ast.Name)]
                    }
                    
                    # Get class methods
                    for item in node.body:
                        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            class_info['methods'].append(item.name)
                    
                    result['classes'].append(class_info)
            
            # Normalize complexity score (0-100)
            total_functions = len(result['functions']) + sum(len(c['methods']) for c in result['classes'])
            if total_functions > 0:
                result['complexity'] = min(100, (result['complexity'] / total_functions) * 10)
            
        except SyntaxError as e:
            logger.error(f"Syntax error in {file_path}: {e}")
        except Exception as e:
            logger.error(f"Error analyzing {file_path}: {e}")
        
        return result
    
    def scan_file(self, file_path: pathlib.Path) -> Optional[FileMetadata]:
        """
        Scan a single file and extract metadata.
        
        Args:
            file_path: Path to file
            
        Returns:
            FileMetadata object or None if file couldn't be scanned
        """
        try:
            # Get file stats
            stat = file_path.stat()
            
            # Count lines
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = sum(1 for _ in f)
            
            # Determine language
            language = self.LANGUAGE_MAP.get(file_path.suffix, 'Unknown')
            
            # Create metadata object
            metadata = FileMetadata(
                path=str(file_path.relative_to(self.root_path)),
                size=stat.st_size,
                lines=lines,
                language=language,
                file_hash=self.calculate_file_hash(file_path)
            )
            
            # Perform deep analysis for Python files
            if file_path.suffix == '.py':
                analysis = self.analyze_python_ast(file_path)
                metadata.imports = analysis['imports']
                metadata.functions = analysis['functions']
                metadata.classes = analysis['classes']
                metadata.complexity_score = analysis['complexity']
            
            return metadata
            
        except Exception as e:
            logger.warning(f"Could not scan {file_path}: {e}")
            return None
    
    def build_dependency_graph(self) -> Dict[str, List[str]]:
        """
        Build a dependency graph showing which files import from which.
        
        Returns:
            Dictionary mapping file paths to lists of their dependencies
        """
        graph = defaultdict(list)
        
        # Create a map of module names to file paths
        module_to_file = {}
        for file_meta in self.structure.files:
            if file_meta.language == 'Python':
                module_name = file_meta.path.replace('/', '.').replace('.py', '')
                module_to_file[module_name] = file_meta.path
        
        # Build the graph
        for file_meta in self.structure.files:
            if file_meta.language == 'Python':
                for import_name in file_meta.imports:
                    # Check if this import corresponds to a local file
                    if import_name in module_to_file:
                        graph[file_meta.path].append(module_to_file[import_name])
        
        return dict(graph)
    
    def scan(self) -> ProjectStructure:
        """
        Perform a complete scan of the project.
        
        Returns:
            ProjectStructure object containing all scan results
        """
        logger.info(f"Starting scan of {self.root_path}")
        
        # Track statistics
        language_counts = defaultdict(int)
        
        # Recursively scan all files
        for root, dirs, files in os.walk(self.root_path, followlinks=self.follow_symlinks):
            current_path = pathlib.Path(root)
            
            # Calculate depth
            try:
                depth = len(current_path.relative_to(self.root_path).parts)
            except ValueError:
                continue
            
            if depth > self.max_depth:
                continue
            
            # Filter out excluded directories
            dirs[:] = [d for d in dirs if not self.should_exclude(current_path / d)]
            
            # Scan each file
            for filename in files:
                file_path = current_path / filename
                
                if self.should_exclude(file_path):
                    continue
                
                # Check if it's a supported file type
                if file_path.suffix not in self.LANGUAGE_MAP:
                    continue
                
                # Scan the file
                metadata = self.scan_file(file_path)
                if metadata:
                    self.structure.files.append(metadata)
                    self.structure.total_lines += metadata.lines
                    language_counts[metadata.language] += 1
        
        # Update structure with aggregated data
        self.structure.total_files = len(self.structure.files)
        self.structure.languages = dict(language_counts)
        self.structure.dependency_graph = self.build_dependency_graph()
        
        logger.info(f"Scan complete: {self.structure.total_files} files, "
                   f"{self.structure.total_lines} lines")
        
        return self.structure
    
    def export_json(self, output_path: str) -> None:
        """
        Export scan results to JSON file.
        
        Args:
            output_path: Path to output JSON file
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.structure.to_dict(), f, indent=2)
        logger.info(f"Exported scan results to {output_path}")


def main():
    """Example usage of the scanner"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python scanner.py <project_path>")
        sys.exit(1)
    
    project_path = sys.argv[1]
    scanner = PulseScanner(project_path)
    structure = scanner.scan()
    
    print(f"\n{'='*60}")
    print(f"📊 Scan Results for: {structure.root_path}")
    print(f"{'='*60}\n")
    print(f"Total Files: {structure.total_files}")
    print(f"Total Lines: {structure.total_lines:,}")
    print(f"\nLanguage Distribution:")
    for lang, count in sorted(structure.languages.items(), key=lambda x: x[1], reverse=True):
        print(f"  • {lang}: {count} files")
    print(f"\nDependencies Found: {len(structure.dependency_graph)} modules")
    
    # Export to JSON
    scanner.export_json('scan_results.json')
    print(f"\n✅ Full results exported to scan_results.json")


if __name__ == '__main__':
    main()
