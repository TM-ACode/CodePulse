/**
 * Example TypeScript File for CodePulse Testing
 * 
 * Demonstrates TypeScript-specific features that CodePulse can analyze.
 */

// Type definitions
interface CodeAnalysisResult {
    score: number;
    grade: string;
    issues: Issue[];
    metrics: CodeMetrics;
}

interface Issue {
    severity: 'critical' | 'high' | 'medium' | 'low';
    category: string;
    message: string;
    line?: number;
}

interface CodeMetrics {
    lines: number;
    functions: number;
    complexity: number;
}

type AnalysisOptions = {
    deep?: boolean;
    includeTests?: boolean;
    maxComplexity?: number;
};

/**
 * Main analyzer class with TypeScript types
 */
class CodeAnalyzer {
    private options: AnalysisOptions;
    private results: CodeAnalysisResult[] = [];

    constructor(options: AnalysisOptions = {}) {
        this.options = {
            deep: false,
            includeTests: true,
            maxComplexity: 10,
            ...options
        };
    }

    /**
     * Analyze a code file
     * @param filePath Path to the file
     * @returns Analysis results
     */
    public async analyzeFile(filePath: string): Promise<CodeAnalysisResult> {
        const content = await this.readFile(filePath);
        const metrics = this.calculateMetrics(content);
        const issues = this.findIssues(content, metrics);
        
        const score = this.calculateScore(metrics, issues);
        const grade = this.calculateGrade(score);

        return {
            score,
            grade,
            issues,
            metrics
        };
    }

    /**
     * Read file content
     */
    private async readFile(path: string): Promise<string> {
        // Implementation would go here
        return '';
    }

    /**
     * Calculate code metrics
     */
    private calculateMetrics(content: string): CodeMetrics {
        const lines = content.split('\n').length;
        const functions = (content.match(/function\s+\w+/g) || []).length;
        const complexity = this.calculateComplexity(content);

        return { lines, functions, complexity };
    }

    /**
     * Calculate cyclomatic complexity
     */
    private calculateComplexity(content: string): number {
        let complexity = 1;
        
        const keywords = ['if', 'else', 'for', 'while', 'case', 'catch'];
        keywords.forEach(keyword => {
            const regex = new RegExp(`\\b${keyword}\\b`, 'g');
            const matches = content.match(regex);
            if (matches) complexity += matches.length;
        });

        return complexity;
    }

    /**
     * Find code issues
     */
    private findIssues(content: string, metrics: CodeMetrics): Issue[] {
        const issues: Issue[] = [];

        // Check complexity
        if (metrics.complexity > (this.options.maxComplexity || 10)) {
            issues.push({
                severity: 'high',
                category: 'complexity',
                message: `Complexity ${metrics.complexity} exceeds threshold`
            });
        }

        // Check for any type usage
        if (content.includes(': any')) {
            issues.push({
                severity: 'medium',
                category: 'types',
                message: 'Avoid using "any" type'
            });
        }

        return issues;
    }

    /**
     * Calculate final score
     */
    private calculateScore(metrics: CodeMetrics, issues: Issue[]): number {
        let score = 100;

        issues.forEach(issue => {
            switch (issue.severity) {
                case 'critical':
                    score -= 25;
                    break;
                case 'high':
                    score -= 15;
                    break;
                case 'medium':
                    score -= 10;
                    break;
                case 'low':
                    score -= 5;
                    break;
            }
        });

        return Math.max(0, score);
    }

    /**
     * Calculate letter grade
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
     * Get all results
     */
    public getResults(): CodeAnalysisResult[] {
        return this.results;
    }
}

// Generic function example
function processArray<T>(items: T[], processor: (item: T) => T): T[] {
    return items.map(processor);
}

// Async function with types
async function fetchAndAnalyze(url: string): Promise<CodeAnalysisResult> {
    const analyzer = new CodeAnalyzer({ deep: true });
    // Fetch code from URL and analyze
    return analyzer.analyzeFile(url);
}

// Export
export { CodeAnalyzer, CodeAnalysisResult, Issue, AnalysisOptions };
export default CodeAnalyzer;
