#!/usr/bin/env python3
"""
Code Analysis Module for Qwen Filesystem Integration
Provides code analysis capabilities without modifying existing filesystem functions.
"""

import re
import os
from typing import Dict, List, Any, Optional
import json

class CodeAnalyzer:
    """Advanced code analysis capabilities for various programming languages."""
    
    def __init__(self):
        self.language_patterns = {
            'python': {
                'functions': r'def\s+(\w+)\s*\(',
                'classes': r'class\s+(\w+)\s*[\(:]',
                'imports': r'(?:from\s+[\w.]+\s+)?import\s+([\w.,\s*]+)',
                'comments': r'#.*$',
                'docstrings': r'"""[\s\S]*?"""'
            },
            'cpp': {
                'functions': r'(?:(?:inline|static|virtual|extern)\s+)*(?:\w+\s+)*(\w+)\s*\([^)]*\)\s*(?:const\s*)?{',
                'classes': r'class\s+(\w+)',
                'includes': r'#include\s*[<"]([^>"]+)[>"]',
                'comments': r'//.*$|/\*[\s\S]*?\*/',
                'namespaces': r'namespace\s+(\w+)'
            },
            'c': {
                'functions': r'(?:(?:static|extern|inline)\s+)*(?:\w+\s+)*(\w+)\s*\([^)]*\)\s*{',
                'structs': r'struct\s+(\w+)',
                'includes': r'#include\s*[<"]([^>"]+)[>"]',
                'comments': r'//.*$|/\*[\s\S]*?\*/',
                'macros': r'#define\s+(\w+)'
            },
            'javascript': {
                'functions': r'(?:function\s+(\w+)|(\w+)\s*=\s*(?:function|\([^)]*\)\s*=>)|(\w+)\s*\([^)]*\)\s*{)',
                'classes': r'class\s+(\w+)',
                'imports': r'(?:import.*?from\s+[\'"]([^\'"]+)[\'"]|import\s+[\'"]([^\'"]+)[\'"])',
                'comments': r'//.*$|/\*[\s\S]*?\*/',
                'exports': r'export\s+(?:default\s+)?(\w+)'
            },
            'java': {
                'classes': r'(?:public\s+)?class\s+(\w+)',
                'methods': r'(?:public|private|protected)?\s*(?:static\s+)?(?:\w+\s+)+(\w+)\s*\([^)]*\)',
                'imports': r'import\s+([\w.]+)',
                'packages': r'package\s+([\w.]+)',
                'comments': r'//.*$|/\*[\s\S]*?\*/'
            }
        }
    
    def detect_language(self, filename: str, content: str) -> str:
        """Detect programming language from filename and content."""
        ext = os.path.splitext(filename)[1].lower()
        
        extension_map = {
            '.py': 'python',
            '.cpp': 'cpp', '.cc': 'cpp', '.cxx': 'cpp',
            '.c': 'c', '.h': 'c',
            '.js': 'javascript', '.jsx': 'javascript',
            '.java': 'java'
        }
        
        if ext in extension_map:
            return extension_map[ext]
            
        # Content-based detection as fallback
        if 'def ' in content and 'import ' in content:
            return 'python'
        elif '#include' in content and ('int main' in content or 'void ' in content):
            return 'cpp' if '::' in content or 'class ' in content else 'c'
        elif 'function ' in content or '=>' in content:
            return 'javascript'
        elif 'public class ' in content:
            return 'java'
            
        return 'unknown'
    
    def analyze_code(self, file_path: str, content: str) -> Dict[str, Any]:
        """Comprehensive code analysis."""
        filename = os.path.basename(file_path)
        language = self.detect_language(filename, content)
        
        analysis = {
            'file_info': {
                'filename': filename,
                'path': file_path,
                'language': language,
                'size_bytes': len(content.encode('utf-8')),
                'line_count': len(content.splitlines())
            },
            'structure': {},
            'metrics': self._calculate_metrics(content),
            'summary': '',
            'dependencies': [],
            'functions': [],
            'classes': []
        }
        
        if language in self.language_patterns:
            patterns = self.language_patterns[language]
            analysis['structure'] = self._extract_structure(content, patterns, language)
            analysis['dependencies'] = self._extract_dependencies(content, patterns, language)
            analysis['functions'] = self._extract_functions(content, patterns, language)
            analysis['classes'] = self._extract_classes(content, patterns, language)
        
        analysis['summary'] = self._generate_summary(analysis)
        return analysis
    
    def explain_code(self, content: str, start_line: int = None, end_line: int = None) -> str:
        """Explain what a piece of code does."""
        lines = content.splitlines()
        
        if start_line is not None and end_line is not None:
            if 1 <= start_line <= len(lines) and 1 <= end_line <= len(lines):
                lines = lines[start_line-1:end_line]
                content = '\n'.join(lines)
        
        explanation = []
        
        # Detect the type of program based on includes/imports
        if '#include <windows.h>' in content or '#include <winsock2.h>' in content:
            explanation.append("This appears to be a Windows systems programming application")
            
            if 'winsock' in content.lower() or 'socket' in content.lower():
                explanation.append("with network/socket programming capabilities")
            if 'registry' in content.lower() or 'winreg' in content.lower():
                explanation.append("that interacts with the Windows registry")
            if 'process' in content.lower() or 'tlhelp32' in content.lower():
                explanation.append("and performs process manipulation or monitoring")
            if 'thread' in content.lower() or '<thread>' in content:
                explanation.append("using multi-threading for concurrent operations")
        
        elif '#include <iostream>' in content and len(lines) < 20:
            explanation.append("This appears to be a simple C++ console application")
        
        elif 'import ' in content and 'def ' in content:
            explanation.append("This is a Python script")
            if 'flask' in content.lower() or 'django' in content.lower():
                explanation.append("for web development")
            elif 'numpy' in content.lower() or 'pandas' in content.lower():
                explanation.append("for data analysis and processing")
        
        elif 'function ' in content or '=>' in content:
            explanation.append("This appears to be JavaScript code")
            if 'react' in content.lower() or 'component' in content.lower():
                explanation.append("likely for a React web application")
            elif 'node' in content.lower() or 'require(' in content:
                explanation.append("for Node.js server-side development")
        
        # Check for main patterns
        if 'def main(' in content or 'int main(' in content:
            explanation.append("The program has a main entry point")
        
        if 'class ' in content:
            classes = re.findall(r'class\s+(\w+)', content)
            if classes:
                explanation.append(f"and defines class(es): {', '.join(classes[:3])}{'...' if len(classes) > 3 else ''}")
        
        if 'def ' in content:
            functions = re.findall(r'def\s+(\w+)', content)
            if functions and len(functions) > 2:
                explanation.append(f"It contains multiple functions including: {', '.join(functions[:3])}{'...' if len(functions) > 3 else ''}")
        
        # Analyze complexity and purpose
        complexity_indicators = content.count('if ') + content.count('for ') + content.count('while ') + content.count('switch ')
        if complexity_indicators > 20:
            explanation.append("The code is complex with significant control flow logic")
        elif complexity_indicators > 5:
            explanation.append("The code has moderate complexity with conditional logic")
        
        # Check for specific patterns that indicate purpose
        if any(word in content.lower() for word in ['server', 'client', 'connect', 'listen', 'bind']):
            explanation.append("It appears to implement network communication functionality")
        
        if any(word in content.lower() for word in ['file', 'read', 'write', 'open', 'close']):
            explanation.append("and includes file I/O operations")
        
        if any(word in content.lower() for word in ['encrypt', 'decrypt', 'hash', 'crypto']):
            explanation.append("with cryptographic or security features")
        
        if any(word in content.lower() for word in ['database', 'sql', 'query', 'table']):
            explanation.append("and interacts with databases")
        
        # Security/system analysis
        if any(word in content.lower() for word in ['privilege', 'admin', 'elevate', 'token']):
            explanation.append("The code may involve privilege escalation or administrative functions")
        
        if any(word in content.lower() for word in ['inject', 'hook', 'patch', 'memory']):
            explanation.append("and appears to perform low-level system manipulation")
        
        if not explanation:
            explanation.append("This code defines custom logic or data structures")
        
        return ". ".join(explanation) + "."
    
    def debug_code(self, file_path: str, content: str) -> Dict[str, Any]:
        """Analyze code for potential bugs and debugging issues."""
        filename = os.path.basename(file_path)
        language = self.detect_language(filename, content)
        
        debug_analysis = {
            'file_info': {
                'filename': filename,
                'path': file_path,
                'language': language,
                'line_count': len(content.splitlines())
            },
            'potential_issues': [],
            'security_concerns': [],
            'memory_issues': [],
            'logic_issues': [],
            'best_practices': [],
            'debugging_suggestions': []
        }
        
        lines = content.splitlines()
        
        # Language-specific debugging analysis
        if language in ['cpp', 'c']:
            debug_analysis.update(self._debug_cpp_code(content, lines))
        elif language == 'python':
            debug_analysis.update(self._debug_python_code(content, lines))
        elif language == 'javascript':
            debug_analysis.update(self._debug_javascript_code(content, lines))
        
        # General debugging checks
        debug_analysis.update(self._debug_general_issues(content, lines))
        
        return debug_analysis
    
    def optimize_code(self, file_path: str, content: str) -> Dict[str, Any]:
        """Analyze code for optimization opportunities."""
        filename = os.path.basename(file_path)
        language = self.detect_language(filename, content)
        
        optimization_analysis = {
            'file_info': {
                'filename': filename,
                'path': file_path,
                'language': language,
                'line_count': len(content.splitlines())
            },
            'performance_opportunities': [],
            'memory_optimizations': [],
            'algorithm_improvements': [],
            'code_structure': [],
            'concurrency_suggestions': [],
            'optimization_priority': 'low'
        }
        
        lines = content.splitlines()
        metrics = self._calculate_metrics(content)
        
        # Language-specific optimization analysis
        if language in ['cpp', 'c']:
            optimization_analysis.update(self._optimize_cpp_code(content, lines, metrics))
        elif language == 'python':
            optimization_analysis.update(self._optimize_python_code(content, lines, metrics))
        elif language == 'javascript':
            optimization_analysis.update(self._optimize_javascript_code(content, lines, metrics))
        
        # General optimization checks
        optimization_analysis.update(self._optimize_general_code(content, lines, metrics))
        
        # Determine optimization priority
        total_suggestions = (len(optimization_analysis['performance_opportunities']) + 
                           len(optimization_analysis['memory_optimizations']) + 
                           len(optimization_analysis['algorithm_improvements']))
        
        if total_suggestions > 10 or metrics['complexity_estimate'] > 50:
            optimization_analysis['optimization_priority'] = 'high'
        elif total_suggestions > 5 or metrics['complexity_estimate'] > 20:
            optimization_analysis['optimization_priority'] = 'medium'
        
        return optimization_analysis
    
    def _calculate_metrics(self, content: str) -> Dict[str, int]:
        """Calculate code metrics."""
        lines = content.splitlines()
        
        metrics = {
            'total_lines': len(lines),
            'non_empty_lines': len([line for line in lines if line.strip()]),
            'comment_lines': len([line for line in lines if line.strip().startswith(('#', '//', '/*'))]),
            'function_count': len(re.findall(r'(?:def |function |int \w+\()', content)),
            'class_count': len(re.findall(r'class\s+\w+', content)),
            'complexity_estimate': content.count('if ') + content.count('for ') + content.count('while ') + content.count('switch ')
        }
        
        metrics['code_lines'] = metrics['non_empty_lines'] - metrics['comment_lines']
        metrics['comment_ratio'] = round(metrics['comment_lines'] / max(metrics['total_lines'], 1) * 100, 1)
        
        return metrics
    
    def _extract_structure(self, content: str, patterns: Dict, language: str) -> Dict:
        """Extract code structure based on language patterns."""
        structure = {}
        
        for element_type, pattern in patterns.items():
            matches = re.findall(pattern, content, re.MULTILINE)
            if matches:
                structure[element_type] = matches
        
        return structure
    
    def _extract_dependencies(self, content: str, patterns: Dict, language: str) -> List[str]:
        """Extract dependencies/imports."""
        dependencies = []
        
        import_pattern = patterns.get('imports') or patterns.get('includes')
        if import_pattern:
            matches = re.findall(import_pattern, content, re.MULTILINE)
            dependencies.extend([match if isinstance(match, str) else match[0] for match in matches])
        
        return list(set(dependencies))
    
    def _extract_functions(self, content: str, patterns: Dict, language: str) -> List[Dict[str, str]]:
        """Extract function information."""
        functions = []
        
        func_pattern = patterns.get('functions')
        if func_pattern:
            for match in re.finditer(func_pattern, content, re.MULTILINE):
                func_name = match.group(1) if match.groups() else match.group(0)
                line_num = content[:match.start()].count('\n') + 1
                
                functions.append({
                    'name': func_name,
                    'line': line_num,
                    'type': 'function'
                })
        
        return functions
    
    def _extract_classes(self, content: str, patterns: Dict, language: str) -> List[Dict[str, str]]:
        """Extract class information."""
        classes = []
        
        class_pattern = patterns.get('classes')
        if class_pattern:
            for match in re.finditer(class_pattern, content, re.MULTILINE):
                class_name = match.group(1)
                line_num = content[:match.start()].count('\n') + 1
                
                classes.append({
                    'name': class_name,
                    'line': line_num,
                    'type': 'class'
                })
        
        return classes
    
    def _generate_summary(self, analysis: Dict) -> str:
        """Generate a human-readable summary."""
        info = analysis['file_info']
        metrics = analysis['metrics']
        
        summary_parts = []
        
        language = info['language']
        dependencies = analysis.get('dependencies', [])
        
        # Language-specific analysis
        if language == 'cpp' or language == 'c':
            if any('windows' in dep.lower() for dep in dependencies):
                summary_parts.append(f"This is a {language.upper()} Windows systems programming application")
            else:
                summary_parts.append(f"This is a {language.upper()} application")
        elif language == 'python':
            summary_parts.append("This is a Python script")
        elif language == 'javascript':
            summary_parts.append("This is a JavaScript application")
        else:
            summary_parts.append(f"This is a {language} file")
        
        # Add size and structure info
        summary_parts.append(f"with {info['line_count']} lines")
        
        # Functions and classes
        if metrics['function_count'] > 0:
            summary_parts.append(f"containing {metrics['function_count']} function(s)")
        
        if metrics['class_count'] > 0:
            summary_parts.append(f"and {metrics['class_count']} class(es)")
        
        # Complexity assessment
        complexity = metrics['complexity_estimate']
        if complexity > 50:
            summary_parts.append(f"The code is highly complex with {complexity} conditional/loop constructs")
        elif complexity > 20:
            summary_parts.append(f"The code has significant complexity with {complexity} control flow constructs")
        elif complexity > 10:
            summary_parts.append(f"The code has moderate complexity with {complexity} conditional/loop constructs")
        elif complexity > 0:
            summary_parts.append(f"The code is relatively simple with {complexity} basic control structures")
        
        return ". ".join(summary_parts) + "."
    
    def _debug_cpp_code(self, content: str, lines: List[str]) -> Dict[str, List[str]]:
        """C++ specific debugging analysis."""
        issues = {
            'potential_issues': [],
            'security_concerns': [],
            'memory_issues': [],
            'logic_issues': [],
            'best_practices': [],
            'debugging_suggestions': []
        }
        
        # Memory management issues
        if 'new ' in content and 'delete ' not in content:
            issues['memory_issues'].append("Potential memory leak: 'new' found but no corresponding 'delete'")
        
        if 'malloc(' in content and 'free(' not in content:
            issues['memory_issues'].append("Potential memory leak: 'malloc' found but no corresponding 'free'")
        
        # Buffer overflow risks
        if any(func in content for func in ['strcpy(', 'strcat(', 'sprintf(', 'gets(']):
            issues['security_concerns'].append("Use of unsafe string functions (strcpy, strcat, sprintf, gets)")
            issues['debugging_suggestions'].append("Consider using safer alternatives: strncpy, strncat, snprintf, fgets")
        
        return issues
    
    def _debug_python_code(self, content: str, lines: List[str]) -> Dict[str, List[str]]:
        """Python specific debugging analysis."""
        issues = {
            'potential_issues': [],
            'security_concerns': [],
            'memory_issues': [],
            'logic_issues': [],
            'best_practices': [],
            'debugging_suggestions': []
        }
        
        # Exception handling
        try_count = content.count('try:')
        except_count = content.count('except')
        if try_count > except_count:
            issues['potential_issues'].append("Some try blocks may be missing except clauses")
        
        # Security issues
        if 'eval(' in content or 'exec(' in content:
            issues['security_concerns'].append("Use of eval() or exec() can be dangerous with untrusted input")
        
        return issues
    
    def _debug_javascript_code(self, content: str, lines: List[str]) -> Dict[str, List[str]]:
        """JavaScript specific debugging analysis."""
        issues = {
            'potential_issues': [],
            'security_concerns': [],
            'memory_issues': [],
            'logic_issues': [],
            'best_practices': [],
            'debugging_suggestions': []
        }
        
        # Variable declaration issues
        if 'var ' in content:
            issues['best_practices'].append("Consider using 'let' or 'const' instead of 'var'")
        
        # Security issues
        if 'eval(' in content:
            issues['security_concerns'].append("eval() can execute arbitrary code - potential security risk")
        
        return issues
    
    def _debug_general_issues(self, content: str, lines: List[str]) -> Dict[str, List[str]]:
        """General debugging issues applicable to all languages."""
        issues = {
            'potential_issues': [],
            'security_concerns': [],
            'memory_issues': [],
            'logic_issues': [],
            'best_practices': [],
            'debugging_suggestions': []
        }
        
        # Code complexity
        if content.count('{') != content.count('}'):
            issues['potential_issues'].append("Mismatched braces - check code structure")
        
        if content.count('(') != content.count(')'):
            issues['potential_issues'].append("Mismatched parentheses")
        
        return issues
    
    def _optimize_cpp_code(self, content: str, lines: List[str], metrics: Dict) -> Dict[str, List[str]]:
        """C++ specific optimization analysis."""
        optimizations = {
            'performance_opportunities': [],
            'memory_optimizations': [],
            'algorithm_improvements': [],
            'code_structure': [],
            'concurrency_suggestions': []
        }
        
        # Vector optimizations
        if 'vector' in content and 'reserve(' not in content:
            optimizations['memory_optimizations'].append("Consider using vector.reserve() to pre-allocate memory")
        
        return optimizations
    
    def _optimize_python_code(self, content: str, lines: List[str], metrics: Dict) -> Dict[str, List[str]]:
        """Python specific optimization analysis."""
        optimizations = {
            'performance_opportunities': [],
            'memory_optimizations': [],
            'algorithm_improvements': [],
            'code_structure': [],
            'concurrency_suggestions': []
        }
        
        # List comprehensions
        nested_loops = content.count('for ') - content.count('[')
        if nested_loops > 0:
            optimizations['performance_opportunities'].append("Consider using list comprehensions for simple loops")
        
        return optimizations
    
    def _optimize_javascript_code(self, content: str, lines: List[str], metrics: Dict) -> Dict[str, List[str]]:
        """JavaScript specific optimization analysis."""
        optimizations = {
            'performance_opportunities': [],
            'memory_optimizations': [],
            'algorithm_improvements': [],
            'code_structure': [],
            'concurrency_suggestions': []
        }
        
        # Array methods
        if 'for(' in content and 'forEach' not in content:
            optimizations['performance_opportunities'].append("Consider using array methods like forEach, map, filter")
        
        return optimizations
    
    def _optimize_general_code(self, content: str, lines: List[str], metrics: Dict) -> Dict[str, List[str]]:
        """General optimization checks applicable to all languages."""
        optimizations = {
            'performance_opportunities': [],
            'memory_optimizations': [],
            'algorithm_improvements': [],
            'code_structure': [],
            'concurrency_suggestions': []
        }
        
        # Function size optimization
        if metrics['complexity_estimate'] > 30:
            optimizations['code_structure'].append("Consider breaking down complex functions into smaller ones")
        
        return optimizations


# Function definitions for integration with existing filesystem handler
def analyze_code(file_path: str) -> Dict[str, Any]:
    """Analyze a code file and return comprehensive analysis."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        analyzer = CodeAnalyzer()
        return analyzer.analyze_code(file_path, content)
    
    except Exception as e:
        return {
            'error': f"Failed to analyze code: {str(e)}",
            'file_path': file_path
        }

def explain_code(file_path: str, start_line: int = None, end_line: int = None) -> str:
    """Explain what a code file or section does."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        analyzer = CodeAnalyzer()
        return analyzer.explain_code(content, start_line, end_line)
    
    except Exception as e:
        return f"Failed to explain code: {str(e)}"

def get_code_metrics(file_path: str) -> Dict[str, int]:
    """Get metrics about a code file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        analyzer = CodeAnalyzer()
        return analyzer.get_code_metrics(content)
    
    except Exception as e:
        return {'error': f"Failed to get metrics: {str(e)}"}

def extract_functions(file_path: str) -> List[Dict[str, str]]:
    """Extract all functions from a code file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        analyzer = CodeAnalyzer()
        language = analyzer.detect_language(file_path, content)
        return analyzer.extract_functions(content, language)
    
    except Exception as e:
        return [{'error': f"Failed to extract functions: {str(e)}"}]

def find_dependencies(file_path: str) -> List[str]:
    """Find all dependencies in a code file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        analyzer = CodeAnalyzer()
        language = analyzer.detect_language(file_path, content)
        return analyzer.find_dependencies(content, language)
    
    except Exception as e:
        return [f"Failed to find dependencies: {str(e)}"]

def debug_code(file_path: str) -> Dict[str, Any]:
    """Analyze code for potential bugs and issues."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        analyzer = CodeAnalyzer()
        return analyzer.debug_code(file_path, content)
    
    except Exception as e:
        return {
            'error': f"Failed to debug code: {str(e)}",
            'file_path': file_path
        }

def optimize_code(file_path: str) -> Dict[str, Any]:
    """Analyze code for optimization opportunities."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        analyzer = CodeAnalyzer()
        return analyzer.optimize_code(file_path, content)
    
    except Exception as e:
        return {
            'error': f"Failed to analyze optimization: {str(e)}",
            'file_path': file_path
        }
