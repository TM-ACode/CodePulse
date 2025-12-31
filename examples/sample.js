/**
 * Example JavaScript File for CodePulse Testing
 * 
 * This file demonstrates what CodePulse can analyze in JavaScript projects.
 */

// Import statements
import express from 'express';
import { readFile } from 'fs/promises';

// Constants
const PORT = 3000;
const API_KEY = 'test-key'; // CodePulse will flag this as a security issue!

/**
 * Main application class
 */
class Application {
    constructor(config) {
        this.config = config;
        this.app = express();
    }

    /**
     * Initialize the application
     */
    async initialize() {
        this.setupRoutes();
        this.setupMiddleware();
        await this.connectDatabase();
    }

    /**
     * Setup Express routes
     */
    setupRoutes() {
        this.app.get('/', (req, res) => {
            res.json({ message: 'Welcome to CodePulse' });
        });

        this.app.get('/analyze', async (req, res) => {
            try {
                const result = await this.performAnalysis(req.query.file);
                res.json(result);
            } catch (error) {
                res.status(500).json({ error: error.message });
            }
        });
    }

    /**
     * Perform code analysis
     * @param {string} filePath - Path to file to analyze
     * @returns {Promise<Object>} Analysis results
     */
    async performAnalysis(filePath) {
        // CodePulse will analyze this function's complexity
        const content = await readFile(filePath, 'utf-8');
        
        let score = 100;
        const issues = [];

        // Check for common issues
        if (content.includes('eval(')) {
            score -= 20;
            issues.push({ type: 'security', message: 'eval() is dangerous' });
        }

        if (content.includes('var ')) {
            score -= 5;
            issues.push({ type: 'style', message: 'Use let/const instead of var' });
        }

        return {
            score,
            issues,
            grade: score >= 80 ? 'A' : 'B'
        };
    }

    /**
     * Connect to database (async example)
     */
    async connectDatabase() {
        return new Promise((resolve) => {
            setTimeout(() => {
                console.log('Database connected');
                resolve();
            }, 1000);
        });
    }

    /**
     * Start the server
     */
    start() {
        this.app.listen(PORT, () => {
            console.log(`Server running on port ${PORT}`);
        });
    }
}

// Export for use in other modules
export default Application;

// Arrow function example
const calculateComplexity = (code) => {
    return code.split('\n').length;
};

// Async arrow function
const fetchData = async (url) => {
    const response = await fetch(url);
    return response.json();
};

export { calculateComplexity, fetchData };
