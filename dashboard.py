#!/usr/bin/env python
"""
Web Dashboard for Codebase Sanity Checker
"""
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import subprocess
import json
import os
import shutil
from pathlib import Path
import tempfile
from datetime import datetime
import threading
import time
import sys
import re

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the core functionality
from run import (
    clone_repo, analyze_structure, run_tests, 
    run_linting, check_dependencies, calculate_score,
    generate_recommendations, generate_report
)

app = Flask(__name__)
CORS(app)

# Store analysis results
analysis_results = {}

def run_analysis(repo_url, task_id):
    """Run the full analysis and store results"""
    try:
        print(f"\n🔍 Starting analysis for: {repo_url}")
        
        # Clone repository
        repo_path = clone_repo(repo_url)
        if not repo_path:
            analysis_results[task_id] = {
                "status": "error",
                "error": "Failed to clone repository"
            }
            return
        
        try:
            # Run all checks
            structure = analyze_structure(repo_path)
            test_results = run_tests(repo_path)
            lint_results = run_linting(repo_path)
            dep_results = check_dependencies(repo_path)
            
            # Prepare results
            results = {
                "repo_url": repo_url,
                "structure": structure,
                "tests": test_results,
                "linting": lint_results,
                "dependencies": dep_results,
                "mode": "advanced"
            }
            
            # Calculate scores
            score = calculate_score(results)
            recommendations = generate_recommendations(results)
            
            # Generate report
            report = generate_report(results)
            
            # Store results
            analysis_results[task_id] = {
                "status": "complete",
                "results": results,
                "score": score,
                "recommendations": recommendations,
                "report": report,
                "timestamp": datetime.now().isoformat()
            }
            
            # Save report to file
            reports_dir = Path("reports")
            reports_dir.mkdir(exist_ok=True)
            report_file = reports_dir / f"report_{task_id}.md"
            report_file.write_text(report)
            
            print(f"✅ Analysis complete: {repo_url}")
            
        finally:
            # Cleanup
            if repo_path and repo_path.exists():
                shutil.rmtree(repo_path, ignore_errors=True)
                
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        analysis_results[task_id] = {
            "status": "error",
            "error": str(e)
        }

@app.route('/')
def index():
    """Home page with dashboard"""
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Start analysis for a repository"""
    data = request.get_json()
    repo_url = data.get('repo_url')
    
    if not repo_url:
        return jsonify({"error": "Repository URL is required"}), 400
    
    # Generate a task ID
    task_id = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Start analysis in background thread
    thread = threading.Thread(target=run_analysis, args=(repo_url, task_id))
    thread.daemon = True
    thread.start()
    
    return jsonify({
        "task_id": task_id,
        "status": "started",
        "message": "Analysis started"
    })

@app.route('/api/status/<task_id>')
def get_status(task_id):
    """Get analysis status"""
    if task_id in analysis_results:
        return jsonify(analysis_results[task_id])
    else:
        return jsonify({"status": "processing"})

@app.route('/api/results/<task_id>')
def get_results(task_id):
    """Get complete analysis results"""
    if task_id not in analysis_results:
        return jsonify({"error": "Results not found"}), 404
    
    results = analysis_results[task_id]
    if results.get('status') == 'complete':
        return jsonify(results)
    else:
        return jsonify({"status": "processing"})

@app.route('/api/download/<task_id>')
def download_report(task_id):
    """Download the generated report"""
    report_file = Path(f"reports/report_{task_id}.md")
    if report_file.exists():
        return send_file(report_file, as_attachment=True)
    else:
        return jsonify({"error": "Report not found"}), 404

def get_breakdown_html(results):
    """Extract scores from results and display breakdown"""
    # Get scores from the results object directly
    report = results.get('report', '')
    
    # Initialize scores
    test_score = '0'
    lint_score = '0'
    struct_score = '0'
    dep_score = '0'
    
    # Parse the report to find scores
    lines = report.split('\n')
    for line in lines:
        if 'Tests:' in line and '/30' in line:
            match = re.search(r'Tests:\s*(\d+)/30', line)
            if match:
                test_score = match.group(1)
        if 'Linting:' in line and '/30' in line:
            match = re.search(r'Linting:\s*(\d+)/30', line)
            if match:
                lint_score = match.group(1)
        if 'Structure:' in line and '/20' in line:
            match = re.search(r'Structure:\s*(\d+)/20', line)
            if match:
                struct_score = match.group(1)
        if 'Dependencies:' in line and '/20' in line:
            match = re.search(r'Dependencies:\s*(\d+)/20', line)
            if match:
                dep_score = match.group(1)
    
    # If parsing failed, try to get from calculate_score breakdown
    if test_score == '0' and lint_score == '0':
        # Fallback: calculate from results
        tests = results.get('tests', {})
        linting = results.get('linting', {})
        structure = results.get('structure', {})
        deps = results.get('dependencies', {})
        
        # Calculate individual scores
        test_status = tests.get('status', '')
        if test_status == 'passed':
            test_score = '30'
        elif test_status == 'failed':
            test_score = '10'
        elif test_status == 'skipped':
            test_score = '15'
        else:
            test_score = '0'
        
        lint_count = linting.get('count', 0)
        if lint_count == 0:
            lint_score = '30'
        elif lint_count <= 5:
            lint_score = '25'
        elif lint_count <= 10:
            lint_score = '20'
        elif lint_count <= 20:
            lint_score = '10'
        else:
            lint_score = '5'
        
        struct_score = '20' if structure.get('python_files', 0) > 0 else '5'
        
        dep_total = deps.get('total', 0)
        dep_score = '15' if dep_total > 0 else '0'
        if deps.get('has_setup_py') or deps.get('has_pyproject'):
            dep_score = str(int(dep_score) + 5)
    
    return f"""
        <h3 style="margin-bottom: 15px;">📊 Score Breakdown</h3>
        <div class="breakdown">
            <div class="breakdown-item">
                <div class="label">🧪 Tests</div>
                <div class="value">{test_score}/30</div>
            </div>
            <div class="breakdown-item">
                <div class="label">🔍 Linting</div>
                <div class="value">{lint_score}/30</div>
            </div>
            <div class="breakdown-item">
                <div class="label">📁 Structure</div>
                <div class="value">{struct_score}/20</div>
            </div>
            <div class="breakdown-item">
                <div class="label">📦 Dependencies</div>
                <div class="value">{dep_score}/20</div>
            </div>
        </div>
    """

# Add the get_breakdown_html function to the template context
@app.context_processor
def utility_processor():
    return dict(get_breakdown_html=get_breakdown_html)

if __name__ == '__main__':
    # Create templates directory
    os.makedirs('templates', exist_ok=True)
    os.makedirs('reports', exist_ok=True)
    
    print("🚀 Starting Codebase Sanity Checker Dashboard")
    print("📍 Open http://localhost:5000 in your browser")
    app.run(debug=True, port=5000)