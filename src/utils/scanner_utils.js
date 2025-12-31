/**
 * CodePulse JavaScript Utilities
 * 
 * Collection of utility functions for code analysis in JavaScript projects.
 * This module provides helpers for scanning, parsing, and analyzing JS code.
 * 
 * @module codepulse/utils
 * @author Saleh Almqati
 * @license MIT
 */

const fs = require('fs').promises;
const path = require('path');
const crypto = require('crypto');

/**
 * File scanner class for JavaScript projects
 */
class FileScanner {
    constructor(rootPath, options = {}) {
        this.rootPath = rootPath;
        this.options = {
            excludePatterns: ['node_modules', '.git', 'dist', 'build'],
            maxDepth: 10,
            followSymlinks: false,
            ...options
        };
        this.results = {
            files: [],
            totalSize: 0,
            languages: {}
        };
    }

    /**
     * Scan directory recursively
     * @param {string} dirPath - Directory to scan
     * @param {number} depth - Current depth
     * @returns {Promise<Object>} Scan results
     */
    async scan(dirPath = this.rootPath, depth = 0) {
        if (depth > this.options.maxDepth) {
            return this.results;
        }

        try {
            const entries = await fs.readdir(dirPath, { withFileTypes: true });

            for (const entry of entries) {
                const fullPath = path.join(dirPath, entry.name);

                // Skip excluded patterns
                if (this.shouldExclude(entry.name)) {
                    continue;
                }

                if (entry.isDirectory()) {
                    await this.scan(fullPath, depth + 1);
                } else if (entry.isFile()) {
                    await this.processFile(fullPath);
                }
            }
        } catch (error) {
            console.error(`Error scanning ${dirPath}:`, error.message);
        }

        return this.results;
    }

    /**
     * Process a single file
     * @param {string} filePath - File to process
     */
    async processFile(filePath) {
        try {
            const stats = await fs.stat(filePath);
            const ext = path.extname(filePath);
            const language = this.detectLanguage(ext);

            const fileInfo = {
                path: filePath,
                name: path.basename(filePath),
                size: stats.size,
                extension: ext,
                language: language,
                modified: stats.mtime
            };

            this.results.files.push(fileInfo);
            this.results.totalSize += stats.size;

            // Update language stats
            if (language) {
                this.results.languages[language] = (this.results.languages[language] || 0) + 1;
            }
        } catch (error) {
            console.error(`Error processing ${filePath}:`, error.message);
        }
    }

    /**
     * Detect language from file extension
     * @param {string} ext - File extension
     * @returns {string|null} Language name
     */
    detectLanguage(ext) {
        const languageMap = {
            '.js': 'JavaScript',
            '.jsx': 'JavaScript',
            '.ts': 'TypeScript',
            '.tsx': 'TypeScript',
            '.py': 'Python',
            '.java': 'Java',
            '.cpp': 'C++',
            '.c': 'C',
            '.go': 'Go',
            '.rs': 'Rust',
            '.rb': 'Ruby',
            '.php': 'PHP'
        };

        return languageMap[ext] || null;
    }

    /**
     * Check if path should be excluded
     * @param {string} name - File or directory name
     * @returns {boolean}
     */
    shouldExclude(name) {
        return this.options.excludePatterns.some(pattern => 
            name.includes(pattern) || name.startsWith('.')
        );
    }

    /**
     * Get scan summary
     * @returns {Object} Summary statistics
     */
    getSummary() {
        return {
            totalFiles: this.results.files.length,
            totalSize: this.formatBytes(this.results.totalSize),
            languages: this.results.languages,
            filesByLanguage: this.groupByLanguage()
        };
    }

    /**
     * Group files by language
     * @returns {Object} Files grouped by language
     */
    groupByLanguage() {
        const grouped = {};
        
        for (const file of this.results.files) {
            const lang = file.language || 'Unknown';
            if (!grouped[lang]) {
                grouped[lang] = [];
            }
            grouped[lang].push(file);
        }

        return grouped;
    }

    /**
     * Format bytes to human-readable format
     * @param {number} bytes - Bytes to format
     * @returns {string} Formatted string
     */
    formatBytes(bytes) {
        if (bytes === 0) return '0 Bytes';
        
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
}

/**
 * Code analyzer class
 */
class CodeAnalyzer {
    constructor() {
        this.patterns = {
            function: /function\s+(\w+)\s*\(/g,
            arrowFunction: /(?:const|let|var)\s+(\w+)\s*=\s*\([^)]*\)\s*=>/g,
            class: /class\s+(\w+)/g,
            import: /import\s+.*?from\s+['"](.+?)['"]/g,
            require: /require\(['"](.+?)['"]\)/g,
            comment: /\/\/.*$|\/\*[\s\S]*?\*\//gm
        };
    }

    /**
     * Analyze JavaScript code
     * @param {string} code - Source code to analyze
     * @returns {Object} Analysis results
     */
    analyze(code) {
        const functions = this.extractFunctions(code);
        const classes = this.extractClasses(code);
        const imports = this.extractImports(code);
        const complexity = this.calculateComplexity(code);
        const metrics = this.calculateMetrics(code);

        return {
            functions,
            classes,
            imports,
            complexity,
            metrics,
            score: this.calculateScore(complexity, metrics)
        };
    }

    /**
     * Extract function names
     * @param {string} code - Source code
     * @returns {Array<string>} Function names
     */
    extractFunctions(code) {
        const functions = [];
        
        // Regular functions
        let match;
        while ((match = this.patterns.function.exec(code)) !== null) {
            functions.push(match[1]);
        }

        // Arrow functions
        this.patterns.arrowFunction.lastIndex = 0;
        while ((match = this.patterns.arrowFunction.exec(code)) !== null) {
            functions.push(match[1]);
        }

        return functions;
    }

    /**
     * Extract class names
     * @param {string} code - Source code
     * @returns {Array<string>} Class names
     */
    extractClasses(code) {
        const classes = [];
        let match;
        
        this.patterns.class.lastIndex = 0;
        while ((match = this.patterns.class.exec(code)) !== null) {
            classes.push(match[1]);
        }

        return classes;
    }

    /**
     * Extract imports and requires
     * @param {string} code - Source code
     * @returns {Array<string>} Import paths
     */
    extractImports(code) {
        const imports = new Set();
        
        // ES6 imports
        let match;
        this.patterns.import.lastIndex = 0;
        while ((match = this.patterns.import.exec(code)) !== null) {
            imports.add(match[1]);
        }

        // CommonJS requires
        this.patterns.require.lastIndex = 0;
        while ((match = this.patterns.require.exec(code)) !== null) {
            imports.add(match[1]);
        }

        return Array.from(imports);
    }

    /**
     * Calculate cyclomatic complexity
     * @param {string} code - Source code
     * @returns {number} Complexity score
     */
    calculateComplexity(code) {
        let complexity = 1; // Base complexity

        const keywords = [
            /\bif\b/g,
            /\belse\b/g,
            /\bfor\b/g,
            /\bwhile\b/g,
            /\bcase\b/g,
            /\bcatch\b/g,
            /\?\s*.*?\s*:/g, // Ternary
            /&&/g,
            /\|\|/g
        ];

        keywords.forEach(pattern => {
            const matches = code.match(pattern);
            if (matches) {
                complexity += matches.length;
            }
        });

        return complexity;
    }

    /**
     * Calculate code metrics
     * @param {string} code - Source code
     * @returns {Object} Metrics
     */
    calculateMetrics(code) {
        const lines = code.split('\n');
        const codeWithoutComments = code.replace(this.patterns.comment, '');
        const codeLines = codeWithoutComments.split('\n').filter(line => 
            line.trim().length > 0
        );

        return {
            totalLines: lines.length,
            codeLines: codeLines.length,
            commentLines: lines.length - codeLines.length,
            averageLineLength: codeLines.reduce((sum, line) => 
                sum + line.length, 0
            ) / codeLines.length || 0
        };
    }

    /**
     * Calculate overall score
     * @param {number} complexity - Complexity score
     * @param {Object} metrics - Code metrics
     * @returns {number} Score (0-100)
     */
    calculateScore(complexity, metrics) {
        let score = 100;

        // Penalize high complexity
        if (complexity > 20) score -= 20;
        else if (complexity > 10) score -= 10;

        // Penalize long functions
        if (metrics.averageLineLength > 100) score -= 10;

        // Reward comments
        const commentRatio = metrics.commentLines / metrics.totalLines;
        if (commentRatio > 0.2) score += 5;

        return Math.max(0, Math.min(100, score));
    }
}

/**
 * Security scanner class
 */
class SecurityScanner {
    constructor() {
        this.vulnerabilities = [];
        this.patterns = {
            eval: /\beval\s*\(/g,
            innerHTML: /\.innerHTML\s*=/g,
            dangerouslySetInnerHTML: /dangerouslySetInnerHTML/g,
            exec: /\bexec\s*\(/g,
            hardcodedSecret: /(?:api[_-]?key|password|secret|token)\s*[:=]\s*['"][^'"]+['"]/gi,
            sqlInjection: /['"].*?\+.*?['"]|`.*?\$\{.*?\}.*?`/g
        };
    }

    /**
     * Scan code for security vulnerabilities
     * @param {string} code - Source code
     * @returns {Array<Object>} Vulnerabilities found
     */
    scan(code) {
        this.vulnerabilities = [];

        this.checkForEval(code);
        this.checkForInnerHTML(code);
        this.checkForExec(code);
        this.checkForHardcodedSecrets(code);
        this.checkForSQLInjection(code);

        return this.vulnerabilities;
    }

    /**
     * Check for eval usage
     * @param {string} code - Source code
     */
    checkForEval(code) {
        if (this.patterns.eval.test(code)) {
            this.vulnerabilities.push({
                type: 'Code Injection',
                severity: 'CRITICAL',
                message: 'eval() usage detected - potential code injection risk',
                recommendation: 'Avoid using eval(). Use safer alternatives.'
            });
        }
    }

    /**
     * Check for innerHTML usage
     * @param {string} code - Source code
     */
    checkForInnerHTML(code) {
        if (this.patterns.innerHTML.test(code) || 
            this.patterns.dangerouslySetInnerHTML.test(code)) {
            this.vulnerabilities.push({
                type: 'XSS',
                severity: 'HIGH',
                message: 'Potential XSS vulnerability with innerHTML',
                recommendation: 'Use textContent or sanitize input'
            });
        }
    }

    /**
     * Check for exec usage
     * @param {string} code - Source code
     */
    checkForExec(code) {
        if (this.patterns.exec.test(code)) {
            this.vulnerabilities.push({
                type: 'Command Injection',
                severity: 'CRITICAL',
                message: 'exec() usage detected - command injection risk',
                recommendation: 'Use safer alternatives or validate input strictly'
            });
        }
    }

    /**
     * Check for hardcoded secrets
     * @param {string} code - Source code
     */
    checkForHardcodedSecrets(code) {
        const matches = code.match(this.patterns.hardcodedSecret);
        if (matches && matches.length > 0) {
            this.vulnerabilities.push({
                type: 'Hardcoded Secret',
                severity: 'CRITICAL',
                message: `Found ${matches.length} potential hardcoded secret(s)`,
                recommendation: 'Use environment variables or secret management'
            });
        }
    }

    /**
     * Check for SQL injection patterns
     * @param {string} code - Source code
     */
    checkForSQLInjection(code) {
        if (this.patterns.sqlInjection.test(code)) {
            this.vulnerabilities.push({
                type: 'SQL Injection',
                severity: 'HIGH',
                message: 'Potential SQL injection vulnerability',
                recommendation: 'Use parameterized queries'
            });
        }
    }

    /**
     * Get security score
     * @returns {number} Score (0-100)
     */
    getSecurityScore() {
        if (this.vulnerabilities.length === 0) return 100;

        let score = 100;
        
        this.vulnerabilities.forEach(vuln => {
            switch (vuln.severity) {
                case 'CRITICAL':
                    score -= 25;
                    break;
                case 'HIGH':
                    score -= 15;
                    break;
                case 'MEDIUM':
                    score -= 10;
                    break;
                case 'LOW':
                    score -= 5;
                    break;
            }
        });

        return Math.max(0, score);
    }
}

/**
 * Report generator class
 */
class ReportGenerator {
    constructor(analysisData) {
        this.data = analysisData;
    }

    /**
     * Generate JSON report
     * @returns {string} JSON report
     */
    generateJSON() {
        return JSON.stringify(this.data, null, 2);
    }

    /**
     * Generate markdown report
     * @returns {string} Markdown report
     */
    generateMarkdown() {
        let report = '# Code Analysis Report\n\n';
        report += `## Summary\n\n`;
        report += `- **Total Files**: ${this.data.totalFiles}\n`;
        report += `- **Total Size**: ${this.data.totalSize}\n`;
        report += `- **Languages**: ${Object.keys(this.data.languages).join(', ')}\n\n`;

        if (this.data.score) {
            report += `## Quality Score: ${this.data.score}/100\n\n`;
        }

        if (this.data.vulnerabilities && this.data.vulnerabilities.length > 0) {
            report += `## Security Issues\n\n`;
            this.data.vulnerabilities.forEach((vuln, i) => {
                report += `${i + 1}. **[${vuln.severity}]** ${vuln.type}\n`;
                report += `   - ${vuln.message}\n`;
                report += `   - *Recommendation*: ${vuln.recommendation}\n\n`;
            });
        }

        return report;
    }

    /**
     * Generate HTML report
     * @returns {string} HTML report
     */
    generateHTML() {
        return `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>CodePulse Analysis Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        h1 { color: #333; }
        .metric { background: #f0f0f0; padding: 10px; margin: 10px 0; }
        .critical { color: #d32f2f; }
        .high { color: #f57c00; }
    </style>
</head>
<body>
    <h1>Code Analysis Report</h1>
    <div class="metric">
        <strong>Total Files:</strong> ${this.data.totalFiles}
    </div>
    <div class="metric">
        <strong>Score:</strong> ${this.data.score || 'N/A'}/100
    </div>
</body>
</html>
        `;
    }
}

// Export modules
module.exports = {
    FileScanner,
    CodeAnalyzer,
    SecurityScanner,
    ReportGenerator
};

// Example usage
if (require.main === module) {
    async function main() {
        const scanner = new FileScanner(process.cwd());
        const results = await scanner.scan();
        console.log('Scan Results:', scanner.getSummary());
    }

    main().catch(console.error);
}
