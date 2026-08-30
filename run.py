#!/usr/bin/env python
"""
Codebase Sanity Checker - Agentic Workflow for Code Analysis
"""
import os
import sys
import subprocess
import tempfile
import shutil
from pathlib import Path
import json
from datetime import datetime
import re
import gc

def clone_repo(repo_url):
    """Clone repository to temp directory"""
    temp_dir = Path(tempfile.mkdtemp())
    print(f"Cloning {repo_url}...")
    
    try:
        result = subprocess.run(
            ["git", "clone", repo_url, str(temp_dir)],
            check=True,
            capture_output=True,
            text=True,
            timeout=120
        )
        print(f"Cloned to {temp_dir}")
        return temp_dir
    except subprocess.CalledProcessError as e:
        print(f"Clone failed: {e.stderr}")
        return None
    except subprocess.TimeoutExpired:
        print("Clone timed out")
        return None

def analyze_structure(repo_path):
    """Analyze repository structure"""
    print("Analyzing repository structure...")
    
    files = []
    dirs = []
    py_files = []
    
    try:
        for item in repo_path.iterdir():
            if item.is_file():
                files.append(item.name)
            elif item.is_dir() and not item.name.startswith('.'):
                dirs.append(item.name)
        
        # Find Python files
        py_files = list(repo_path.rglob("*.py"))
        
        # Read README if exists
        readme = ""
        readme_path = repo_path / "README.md"
        if readme_path.exists():
            try:
                readme = readme_path.read_text(encoding='utf-8')[:500]
            except:
                pass
        
        return {
            "files": files[:20],
            "directories": dirs[:10],
            "python_files": len(py_files),
            "readme_preview": readme,
            "structure_summary": f"{len(dirs)} directories, {len(files)} files, {len(py_files)} Python files"
        }
    except Exception as e:
        print(f"Error analyzing structure: {e}")
        return {"error": str(e)}

def run_tests(repo_path):
    """Run pytest if available"""
    print("Running tests...")
    
    # First check if pytest is available
    try:
        subprocess.run(["pytest", "--version"], capture_output=True, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("pytest not found - skipping tests")
        return {"status": "skipped", "error": "pytest not installed"}
    
    try:
        result = subprocess.run(
            ["pytest", str(repo_path), "-v", "--tb=short", "-x", "--maxfail=5"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print("All tests passed!")
            return {"status": "passed", "output": result.stdout[:500]}
        else:
            print("Tests failed")
            return {"status": "failed", "output": result.stdout[:500], "error": result.stderr[:500]}
    except subprocess.TimeoutExpired:
        print("Tests timed out")
        return {"status": "timeout", "error": "Tests took too long"}
    except Exception as e:
        print(f"Test execution error: {e}")
        return {"status": "error", "error": str(e)}

def run_linting(repo_path):
    """Run flake8 if available"""
    print("Running linters...")
    
    # Check if flake8 is available
    try:
        subprocess.run(["flake8", "--version"], capture_output=True, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print(" flake8 not found - skipping linting")
        return {"issues": [], "count": 0, "error": "flake8 not installed"}
    
    try:
        result = subprocess.run(
            ["flake8", str(repo_path), "--max-line-length=120", "--count"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        issues = [line.strip() for line in result.stdout.split("\n") if line.strip() and not line.startswith(" ")]
        
        # Remove the count line if present
        if issues and issues[-1].isdigit():
            issues.pop()
        
        if issues:
            print(f" Found {len(issues)} linting issues")
            return {"issues": issues[:10], "count": len(issues)}
        else:
            print(" No linting issues found")
            return {"issues": [], "count": 0}
    except subprocess.TimeoutExpired:
        print("  Linting timed out")
        return {"issues": [], "count": 0, "error": "timed out"}
    except Exception as e:
        print(f"  Linting error: {e}")
        return {"issues": [], "count": 0, "error": str(e)}

def check_dependencies(repo_path):
    """Check Python dependencies"""
    print(" Checking dependencies...")
    
    deps = []
    req_file = repo_path / "requirements.txt"
    if req_file.exists():
        try:
            content = req_file.read_text()
            deps = [line.strip() for line in content.split("\n") 
                   if line.strip() and not line.startswith("#")]
            print(f"Found {len(deps)} dependencies")
        except:
            print("  Error reading requirements.txt")
    else:
        print("No requirements.txt found")
    
    # Check for other package files
    has_setup_py = (repo_path / "setup.py").exists()
    has_pyproject = (repo_path / "pyproject.toml").exists()
    
    return {
        "dependencies": deps[:20],
        "has_setup_py": has_setup_py,
        "has_pyproject": has_pyproject,
        "total": len(deps)
    }

def generate_report(results):
    """Generate a markdown report"""
    repo_name = results.get("repo_url", "unknown").split("/")[-1].replace(".git", "")
    
    report = f"""# Codebase Health Report

**Repository:** {repo_name}
**Analyzed:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Mode:** {results.get('mode', 'baseline').upper()}

---

## Summary

| Metric | Value |
|--------|-------|
| **Tests** | {results.get('tests', {}).get('status', 'Unknown')} |
| **Linting Issues** | {results.get('linting', {}).get('count', 0)} |
| **Python Files** | {results.get('structure', {}).get('python_files', 0)} |
| **Dependencies** | {results.get('dependencies', {}).get('total', 0)} |

---

## Repository Structure

{results.get('structure', {}).get('structure_summary', 'No structure info')}

### Key Files
{', '.join(results.get('structure', {}).get('files', [])[:8])}

### Directories
{', '.join(results.get('structure', {}).get('directories', [])[:5])}

---

## Test Results

**Status:** {results.get('tests', {}).get('status', 'Unknown')}

"""
    test_output = results.get('tests', {}).get('output', '')
    if test_output:
        report += f"""
	{test_output}
"""
    else:
        report += "No test output available\n"

    report += f"""

## Linting Issues

**Total Issues Found:** {results.get('linting', {}).get('count', 0)}

"""
    issues = results.get('linting', {}).get('issues', [])
    if issues:
        for issue in issues[:10]:
            report += f"- `{issue}`\n"
        if len(issues) > 10:
            report += f"\n*... and {len(issues) - 10} more issues*"
    else:
        report += "No linting issues found\n"

    report += f"""

## Dependencies

**Total:** {results.get('dependencies', {}).get('total', 0)}

"""
    deps = results.get('dependencies', {}).get('dependencies', [])
    if deps:
        for dep in deps[:10]:
            report += f"- {dep}\n"
        if len(deps) > 10:
            report += f"\n*... and {len(deps) - 10} more*"
    else:
        report += "No dependencies listed\n"

    if results.get('dependencies', {}).get('has_setup_py'):
        report += "\n Setup.py found\n"
    if results.get('dependencies', {}).get('has_pyproject'):
        report += "\n pyproject.toml found\n"

    report += f"""

## Quality Score

**Overall Score:** {calculate_score(results)}/100

### Breakdown
- Tests: {get_test_score(results.get('tests', {}))}/30
- Linting: {get_lint_score(results.get('linting', {}))}/30
- Structure: {get_structure_score(results.get('structure', {}))}/20
- Dependencies: {get_dependency_score(results.get('dependencies', {}))}/20

---

## Recommendations

{generate_recommendations(results)}

---

*Report generated by Codebase Sanity Checker - Agentic Workflow*
"""
    
    return report

def calculate_score(results):
    """Calculate overall quality score"""
    score = 0
    
    # Test score (max 30)
    test_status = results.get('tests', {}).get('status', '')
    if test_status == 'passed':
        score += 30
    elif test_status == 'failed':
        score += 10
    elif test_status == 'skipped':
        score += 15
    
    # Linting score (max 30)
    lint_count = results.get('linting', {}).get('count', 0)
    if lint_count == 0:
        score += 30
    elif lint_count <= 5:
        score += 25
    elif lint_count <= 10:
        score += 20
    elif lint_count <= 20:
        score += 10
    else:
        score += 5
    
    # Structure score (max 20)
    py_files = results.get('structure', {}).get('python_files', 0)
    if py_files > 0:
        score += 20
    
    # Dependency score (max 20)
    deps = results.get('dependencies', {}).get('total', 0)
    if deps > 0:
        score += 15
    if results.get('dependencies', {}).get('has_setup_py') or results.get('dependencies', {}).get('has_pyproject'):
        score += 5
    
    return min(100, score)

def get_test_score(tests):
    """Get test score component"""
    status = tests.get('status', '')
    if status == 'passed':
        return 30
    elif status == 'failed':
        return 10
    elif status == 'skipped':
        return 15
    return 0

def get_lint_score(linting):
    """Get linting score component"""
    count = linting.get('count', 0)
    if count == 0:
        return 30
    elif count <= 5:
        return 25
    elif count <= 10:
        return 20
    elif count <= 20:
        return 10
    return 5

def get_structure_score(structure):
    """Get structure score component"""
    if structure.get('python_files', 0) > 0:
        return 20
    return 5

def get_dependency_score(deps):
    """Get dependency score component"""
    score = 0
    if deps.get('total', 0) > 0:
        score += 15
    if deps.get('has_setup_py') or deps.get('has_pyproject'):
        score += 5
    return score

def generate_recommendations(results):
    """Generate actionable recommendations"""
    recommendations = []
    
    # Test recommendations
    test_status = results.get('tests', {}).get('status', '')
    if test_status == 'failed':
        recommendations.append(" Fix failing tests: Some tests are failing. Run pytest locally to identify issues.")
    elif test_status == 'skipped':
        recommendations.append(" Add tests: Consider adding tests to improve code quality and reliability.")
    elif test_status == 'passed':
        recommendations.append(" Tests passing: Good job! Keep maintaining test coverage.")
    
    # Linting recommendations
    lint_count = results.get('linting', {}).get('count', 0)
    if lint_count > 10:
        recommendations.append(f" Fix linting issues: Found {lint_count} linting issues. Run flake8 to fix them.")
    elif lint_count > 0:
        recommendations.append(f" Address linting: Found {lint_count} minor issues. Consider fixing them.")
    else:
        recommendations.append(" Clean code: No linting issues found!")
    
    # Structure recommendations
    py_files = results.get('structure', {}).get('python_files', 0)
    if py_files == 0:
        recommendations.append(" No Python files found: This might not be a Python repository.")
    
    # Dependency recommendations
    deps = results.get('dependencies', {})
    if deps.get('total', 0) == 0 and py_files > 0:
        recommendations.append(" Missing requirements.txt: Consider adding requirements.txt for dependency management.")
    elif deps.get('total', 0) > 0:
        recommendations.append(f" Dependencies: {deps.get('total', 0)} dependencies found. Keep them updated.")
    
    if not recommendations:
        recommendations.append(" Everything looks good! The codebase appears well-maintained.")
    
    return "\n".join([f"{i+1}. {rec}" for i, rec in enumerate(recommendations)])

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Codebase Sanity Checker")
    parser.add_argument("--repo", required=True, help="GitHub repository URL")
    parser.add_argument("--output", help="Output directory for reports")
    parser.add_argument("--advanced", action="store_true", help="Use advanced analysis mode")
    
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("CODEBASE SANITY CHECKER")
    print("="*60)
    print(f"Repository: {args.repo}")
    print(f"Mode: {'Advanced' if args.advanced else 'Baseline'}")
    print("-"*60)
    
    # Clone repo
    repo_path = clone_repo(args.repo)
    if not repo_path:
        print("Failed to clone repository. Exiting.")
        sys.exit(1)
    
    try:
        # Run checks
        structure = analyze_structure(repo_path)
        test_results = run_tests(repo_path)
        lint_results = run_linting(repo_path)
        dep_results = check_dependencies(repo_path)
        
        # Prepare results
        results = {
            "repo_url": args.repo,
            "structure": structure,
            "tests": test_results,
            "linting": lint_results,
            "dependencies": dep_results,
            "mode": "advanced" if args.advanced else "baseline"
        }
        
        # Generate report
        report = generate_report(results)
        
        # Save report if output specified
        if args.output:
            output_path = Path(args.output)
            output_path.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_file = output_path / f"report_{timestamp}.md"
            report_file.write_text(report)
            print(f"\nReport saved to: {report_file}")
        
        # Print report
        print("\n" + "="*60)
        print("FINAL REPORT")
        print("="*60)
        print(report)
        
        # Save results as JSON for later analysis
        json_file = Path("latest_results.json")
        json_file.write_text(json.dumps(results, indent=2, default=str))
        print(f"\nResults saved to: {json_file}")
        
    finally:
        # Cleanup
        print("\nCleaning up...")
        if repo_path and repo_path.exists():
            try:
                # Force close any open handles
                gc.collect()
                shutil.rmtree(repo_path, ignore_errors=True)
                print("Cleanup complete")
            except Exception as e:
                print(f"Note: Cleanup had issues (not critical): {e}")
    
    print("\nAnalysis complete!")
    print("="*60)

if __name__ == "__main__":
    main()