/**
 * CodePulse TypeScript Analysis Engine
 * 
 * Type-safe code analysis utilities for TypeScript projects.
 * Provides interfaces, types, and classes for comprehensive code analysis.
 * 
 * @module codepulse/analyzer
 * @author Saleh Almqati
 * @license MIT
 */

import { promises as fs } from 'fs';
import * as path from 'path';

// ============================================================================
// Type Definitions
// ============================================================================

/**
 * Severity levels for issues
 */
export enum Severity {
    CRITICAL = 'critical',
    HIGH = 'high',
    MEDIUM = 'medium',
    LOW = 'low',
    INFO = 'info'
}

/**
 * Issue categories
 */
export enum IssueCategory {
    SECURITY = 'security',
    PERFORMANCE = 'performance',
    STYLE = 'style',
    COMPLEXITY = 'complexity',
    MAINTAINABILITY = 'maintainability',
    DOCUMENTATION = 'documentation'
}

/**
 * Analysis options interface
 */
export interface AnalysisOptions {
    deep?: boolean;
    includeTests?: boolean;
    excludePatterns?: string[];
    maxComplexity?: number;
    enableAI?: boolean;
    securityLevel?: 'basic' | 'standard' | 'strict';
}

/**
 * File metadata interface
 */
export interface FileMetadata {
    path: string;
    name: string;
    extension: string;
    language: string;
    size: number;
    lines: number;
    codeLines: number;
    commentLines: number;
    hash: string;
    lastModified: Date;
}

/**
 * Code issue interface
 */
export interface CodeIssue {
    id: string;
    severity: Severity;
    category: IssueCategory;
    title: string;
    description: string;
    file: string;
    line?: number;
    column?: number;
    recommendation?: string;
    cweId?: string;
}

/**
 * Code metrics interface
 */
export interface CodeMetrics {
    cyclomaticComplexity: number;
    cognitiveComplexity: number;
    linesOfCode: number;
    maintainabilityIndex: number;
    functionCount: number;
    classCount: number;
    averageFunctionLength: number;
    maxNestingDepth: number;
}

/**
 * Analysis result interface
 */
export interface AnalysisResult {
    timestamp: Date;
    projectPath: string;
    totalFiles: number;
    totalLines: number;
    languages: Record<string, number>;
    overallScore: number;
    grade: string;
    metrics: CodeMetrics;
    issues: CodeIssue[];
    vulnerabilities: SecurityVulnerability[];
    recommendations: string[];
}

/**
 * Security vulnerability interface
 */
export interface SecurityVulnerability {
    id: string;
    type: string;
    severity: Severity;
    title: string;
    description: string;
    file: string;
    line?: number;
    cweId: string;
    cvssScore?: number;
    recommendation: string;
}

/**
 * Dependency information interface
 */
export interface DependencyInfo {
    name: string;
    version: string;
    type: 'production' | 'development';
    vulnerabilities: SecurityVulnerability[];
    outdated: boolean;
    license?: string;
}

// ============================================================================
// Main Analyzer Class
// ============================================================================

/**
 * Main code analyzer class with full TypeScript support
 */
export class PulseAnalyzer {
    private options: Required<AnalysisOptions>;
    private results: Partial<AnalysisResult>;
    private fileCache: Map<string, FileMetadata>;

    constructor(options: AnalysisOptions = {}) {
        this.options = {
            deep: false,
            includeTests: true,
            excludePatterns: ['node_modules', 'dist', 'build', '.git'],
            maxComplexity: 10,
            enableAI: false,
            securityLevel: 'standard',
            ...options
        };

        this.results = {
            timestamp: new Date(),
            issues: [],
            vulnerabilities: [],
            recommendations: []
        };

        this.fileCache = new Map();
    }

    /**
     * Analyze a project directory
     * @param projectPath Path to project root
     * @returns Complete analysis results
     */
    public async analyzeProject(projectPath: string): Promise<AnalysisResult> {
        console.log(`Analyzing project: ${projectPath}`);

        this.results.projectPath = projectPath;

        // Step 1: Scan all files
        const files = await this.scanDirectory(projectPath);
        this.results.totalFiles = files.length;

        // Step 2: Calculate metrics
        const metrics = await this.calculateProjectMetrics(files);
        this.results.metrics = metrics;

        // Step 3: Analyze each file
        for (const file of files) {
            await this.analyzeFile(file);
        }

        // Step 4: Run security analysis
        await this.performSecurityAnalysis(files);

        // Step 5: Calculate scores
        this.calculateScores();

        // Step 6: Generate recommendations
        this.generateRecommendations();

        return this.results as AnalysisResult;
    }

    /**
     * Scan directory recursively
     * @param dirPath Directory to scan
     * @returns Array of file metadata
     */
    private async scanDirectory(dirPath: string): Promise<FileMetadata[]> {
        const files: FileMetadata[] = [];

        const scan = async (currentPath: string): Promise<void> => {
            try {
                const entries = await fs.readdir(currentPath, { withFileTypes: true });

                for (const entry of entries) {
                    const fullPath = path.join(currentPath, entry.name);

                    if (this.shouldExclude(entry.name)) {
                        continue;
                    }

                    if (entry.isDirectory()) {
                        await scan(fullPath);
                    } else if (entry.isFile()) {
                        const metadata = await this.extractFileMetadata(fullPath);
                        if (metadata) {
                            files.push(metadata);
                            this.fileCache.set(fullPath, metadata);
                        }
                    }
                }
            } catch (error) {
                console.error(`Error scanning ${currentPath}:`, error);
            }
        };

        await scan(dirPath);
        return files;
    }

    /**
     * Extract file metadata
     * @param filePath Path to file
     * @returns File metadata or null
     */
    private async extractFileMetadata(filePath: string): Promise<FileMetadata | null> {
        try {
            const stats = await fs.stat(filePath);
            const content = await fs.readFile(filePath, 'utf-8');
            const lines = content.split('\n');

            const codeLines = this.countCodeLines(lines);
            const commentLines = lines.length - codeLines;

            return {
                path: filePath,
                name: path.basename(filePath),
                extension: path.extname(filePath),
                language: this.detectLanguage(path.extname(filePath)),
                size: stats.size,
                lines: lines.length,
                codeLines,
                commentLines,
                hash: this.calculateHash(content),
                lastModified: stats.mtime
            };
        } catch (error) {
            console.error(`Error reading ${filePath}:`, error);
            return null;
        }
    }

    /**
     * Analyze a single file
     * @param file File metadata
     */
    private async analyzeFile(file: FileMetadata): Promise<void> {
        try {
            const content = await fs.readFile(file.path, 'utf-8');

            // Check for common issues
            this.checkForLongFunctions(content, file);
            this.checkForComplexity(content, file);
            this.checkForBadPractices(content, file);
            this.checkForMissingDocumentation(content, file);

        } catch (error) {
            console.error(`Error analyzing ${file.path}:`, error);
        }
    }

    /**
     * Check for long functions
     * @param content File content
     * @param file File metadata
     */
    private checkForLongFunctions(content: string, file: FileMetadata): void {
        const functionPattern = /function\s+\w+\s*\([^)]*\)\s*\{/g;
        let match;

        while ((match = functionPattern.exec(content)) !== null) {
            const start = match.index;
            const end = this.findClosingBrace(content, start);
            const functionLength = content.substring(start, end).split('\n').length;

            if (functionLength > 50) {
                this.addIssue({
                    id: this.generateId(),
                    severity: Severity.MEDIUM,
                    category: IssueCategory.MAINTAINABILITY,
                    title: 'Long Function Detected',
                    description: `Function is ${functionLength} lines long. Consider breaking it down.`,
                    file: file.path,
                    recommendation: 'Split large functions into smaller, focused functions'
                });
            }
        }
    }

    /**
     * Check for high complexity
     * @param content File content
     * @param file File metadata
     */
    private checkForComplexity(content: string, file: FileMetadata): void {
        const complexity = this.calculateCyclomaticComplexity(content);

        if (complexity > this.options.maxComplexity) {
            this.addIssue({
                id: this.generateId(),
                severity: Severity.HIGH,
                category: IssueCategory.COMPLEXITY,
                title: 'High Cyclomatic Complexity',
                description: `Complexity score of ${complexity} exceeds threshold of ${this.options.maxComplexity}`,
                file: file.path,
                recommendation: 'Refactor to reduce complexity'
            });
        }
    }

    /**
     * Check for bad practices
     * @param content File content
     * @param file File metadata
     */
    private checkForBadPractices(content: string, file: FileMetadata): void {
        // Check for var usage
        if (content.match(/\bvar\s+/g)) {
            this.addIssue({
                id: this.generateId(),
                severity: Severity.LOW,
                category: IssueCategory.STYLE,
                title: 'Use of var keyword',
                description: 'var keyword detected. Use let or const instead.',
                file: file.path,
                recommendation: 'Replace var with let or const'
            });
        }

        // Check for console.log
        if (content.match(/console\.log/g)) {
            this.addIssue({
                id: this.generateId(),
                severity: Severity.INFO,
                category: IssueCategory.STYLE,
                title: 'Console.log statement',
                description: 'Remove console.log before production',
                file: file.path,
                recommendation: 'Use proper logging library'
            });
        }
    }

    /**
     * Check for missing documentation
     * @param content File content
     * @param file File metadata
     */
    private checkForMissingDocumentation(content: string, file: FileMetadata): void {
        const functions = content.match(/function\s+\w+/g) || [];
        const docComments = content.match(/\/\*\*[\s\S]*?\*\//g) || [];

        if (functions.length > docComments.length) {
            this.addIssue({
                id: this.generateId(),
                severity: Severity.LOW,
                category: IssueCategory.DOCUMENTATION,
                title: 'Missing Documentation',
                description: `${functions.length - docComments.length} functions lack documentation`,
                file: file.path,
                recommendation: 'Add JSDoc comments to functions'
            });
        }
    }

    /**
     * Perform security analysis
     * @param files Array of file metadata
     */
    private async performSecurityAnalysis(files: FileMetadata[]): Promise<void> {
        for (const file of files) {
            try {
                const content = await fs.readFile(file.path, 'utf-8');
                this.checkSecurityIssues(content, file);
            } catch (error) {
                console.error(`Error in security analysis for ${file.path}:`, error);
            }
        }
    }

    /**
     * Check for security issues
     * @param content File content
     * @param file File metadata
     */
    private checkSecurityIssues(content: string, file: FileMetadata): void {
        // Check for hardcoded secrets
        const secretPattern = /(?:api[_-]?key|password|secret|token)\s*[:=]\s*['"][^'"]+['"]/gi;
        if (secretPattern.test(content)) {
            this.addVulnerability({
                id: this.generateId(),
                type: 'Hardcoded Secret',
                severity: Severity.CRITICAL,
                title: 'Hardcoded Secret Detected',
                description: 'Sensitive credentials found in code',
                file: file.path,
                cweId: 'CWE-798',
                recommendation: 'Use environment variables or secret management'
            });
        }

        // Check for eval usage
        if (content.includes('eval(')) {
            this.addVulnerability({
                id: this.generateId(),
                type: 'Code Injection',
                severity: Severity.CRITICAL,
                title: 'Dangerous eval() Usage',
                description: 'eval() can execute arbitrary code',
                file: file.path,
                cweId: 'CWE-94',
                recommendation: 'Avoid eval(). Use safer alternatives'
            });
        }
    }

    /**
     * Calculate project metrics
     * @param files Array of file metadata
     * @returns Code metrics
     */
    private async calculateProjectMetrics(files: FileMetadata[]): Promise<CodeMetrics> {
        let totalComplexity = 0;
        let totalFunctions = 0;
        let totalClasses = 0;
        let totalFunctionLength = 0;

        for (const file of files) {
            try {
                const content = await fs.readFile(file.path, 'utf-8');
                totalComplexity += this.calculateCyclomaticComplexity(content);
                
                const functions = (content.match(/function\s+\w+/g) || []).length;
                const classes = (content.match(/class\s+\w+/g) || []).length;
                
                totalFunctions += functions;
                totalClasses += classes;
            } catch (error) {
                // Skip file
            }
        }

        const totalLines = files.reduce((sum, f) => sum + f.lines, 0);
        const avgFunctionLength = totalFunctions > 0 ? totalLines / totalFunctions : 0;

        return {
            cyclomaticComplexity: totalComplexity,
            cognitiveComplexity: totalComplexity * 1.2,
            linesOfCode: files.reduce((sum, f) => sum + f.codeLines, 0),
            maintainabilityIndex: this.calculateMaintainabilityIndex(totalComplexity, totalLines),
            functionCount: totalFunctions,
            classCount: totalClasses,
            averageFunctionLength: Math.round(avgFunctionLength),
            maxNestingDepth: 5 // Simplified
        };
    }

    /**
     * Calculate cyclomatic complexity
     * @param content Source code
     * @returns Complexity score
     */
    private calculateCyclomaticComplexity(content: string): number {
        let complexity = 1;

        const patterns = [
            /\bif\b/g,
            /\belse\b/g,
            /\bfor\b/g,
            /\bwhile\b/g,
            /\bcase\b/g,
            /\bcatch\b/g,
            /\?\s*.*?\s*:/g,
            /&&/g,
            /\|\|/g
        ];

        patterns.forEach(pattern => {
            const matches = content.match(pattern);
            if (matches) complexity += matches.length;
        });

        return complexity;
    }

    /**
     * Calculate maintainability index
     * @param complexity Cyclomatic complexity
     * @param lines Lines of code
     * @returns Maintainability index
     */
    private calculateMaintainabilityIndex(complexity: number, lines: number): number {
        // Simplified maintainability index
        const volume = lines * Math.log2(lines + 1);
        const mi = 171 - 5.2 * Math.log(volume) - 0.23 * complexity - 16.2 * Math.log(lines);
        return Math.max(0, Math.min(100, mi));
    }

    /**
     * Calculate overall scores
     */
    private calculateScores(): void {
        const issueWeight = {
            [Severity.CRITICAL]: 25,
            [Severity.HIGH]: 15,
            [Severity.MEDIUM]: 10,
            [Severity.LOW]: 5,
            [Severity.INFO]: 1
        };

        let score = 100;

        // Deduct for issues
        this.results.issues?.forEach(issue => {
            score -= issueWeight[issue.severity];
        });

        // Deduct for vulnerabilities
        this.results.vulnerabilities?.forEach(vuln => {
            score -= issueWeight[vuln.severity];
        });

        this.results.overallScore = Math.max(0, score);
        this.results.grade = this.calculateGrade(this.results.overallScore);
    }

    /**
     * Calculate letter grade
     * @param score Numerical score
     * @returns Letter grade
     */
    private calculateGrade(score: number): string {
        if (score >= 90) return 'A+';
        if (score >= 85) return 'A';
        if (score >= 80) return 'B+';
        if (score >= 75) return 'B';
        if (score >= 70) return 'C+';
        if (score >= 60) return 'C';
        return 'D';
    }

    /**
     * Generate recommendations
     */
    private generateRecommendations(): void {
        const recommendations: string[] = [];

        // Based on issues
        if (this.results.issues && this.results.issues.length > 0) {
            const criticalIssues = this.results.issues.filter(i => i.severity === Severity.CRITICAL);
            if (criticalIssues.length > 0) {
                recommendations.push(`Fix ${criticalIssues.length} critical issue(s) immediately`);
            }
        }

        // Based on metrics
        if (this.results.metrics) {
            if (this.results.metrics.averageFunctionLength > 50) {
                recommendations.push('Break down large functions into smaller ones');
            }

            if (this.results.metrics.maintainabilityIndex < 50) {
                recommendations.push('Improve code maintainability through refactoring');
            }
        }

        // Based on vulnerabilities
        if (this.results.vulnerabilities && this.results.vulnerabilities.length > 0) {
            recommendations.push('Address all security vulnerabilities before deployment');
        }

        this.results.recommendations = recommendations;
    }

    // Helper methods

    private shouldExclude(name: string): boolean {
        return this.options.excludePatterns.some(pattern => 
            name.includes(pattern) || name.startsWith('.')
        );
    }

    private detectLanguage(ext: string): string {
        const map: Record<string, string> = {
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.jsx': 'JavaScript',
            '.tsx': 'TypeScript',
            '.py': 'Python',
            '.java': 'Java'
        };
        return map[ext] || 'Unknown';
    }

    private countCodeLines(lines: string[]): number {
        return lines.filter(line => {
            const trimmed = line.trim();
            return trimmed.length > 0 && !trimmed.startsWith('//') && !trimmed.startsWith('/*');
        }).length;
    }

    private calculateHash(content: string): string {
        // Simplified hash
        return Buffer.from(content).toString('base64').substring(0, 16);
    }

    private findClosingBrace(content: string, start: number): number {
        let depth = 0;
        for (let i = start; i < content.length; i++) {
            if (content[i] === '{') depth++;
            if (content[i] === '}') {
                depth--;
                if (depth === 0) return i;
            }
        }
        return content.length;
    }

    private generateId(): string {
        return `ISSUE-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    }

    private addIssue(issue: CodeIssue): void {
        if (!this.results.issues) this.results.issues = [];
        this.results.issues.push(issue);
    }

    private addVulnerability(vuln: SecurityVulnerability): void {
        if (!this.results.vulnerabilities) this.results.vulnerabilities = [];
        this.results.vulnerabilities.push(vuln);
    }
}

// Export for external use
export default PulseAnalyzer;
