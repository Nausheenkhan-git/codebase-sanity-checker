#!/usr/bin/env python
"""
Batch testing script for Codebase Sanity Checker
Runs analysis on multiple repositories and generates reports
"""
import subprocess
import json
import time
from pathlib import Path

# List of repositories to test
REPOSITORIES = [
    "https://github.com/psf/requests.git",
    "https://github.com/realpython/python-guide.git",
    "https://github.com/pallets/flask.git",
    "https://github.com/django/django.git",
    "https://github.com/pytest-dev/pytest.git",
    "https://github.com/encode/httpx.git",
    "https://github.com/pydantic/pydantic.git",
    "https://github.com/tiangolo/fastapi.git",
]

def test_repository(repo_url, output_dir="./reports"):
    """Test a single repository"""
    print(f"\n{'='*60}")
    print(f"Testing: {repo_url}")
    print(f"{'='*60}")
    
    try:
        # Run the checker
        result = subprocess.run(
            ["python", "run.py", "--repo", repo_url, "--output", output_dir],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode == 0:
            print(f" Success: {repo_url}")
        else:
            print(f" Failed: {repo_url}")
            print(result.stderr)
            
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print(f" Timeout: {repo_url}")
        return False
    except Exception as e:
        print(f" Error: {repo_url} - {e}")
        return False

def main():
    """Run tests on all repositories"""
    print(" Starting batch testing...")
    print(f" Testing {len(REPOSITORIES)} repositories")
    
    results = []
    start_time = time.time()
    
    for i, repo in enumerate(REPOSITORIES, 1):
        print(f"\n[{i}/{len(REPOSITORIES)}] Testing...")
        success = test_repository(repo)
        results.append({
            "repository": repo,
            "success": success,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        })
        time.sleep(2)  # Rate limiting
    
    elapsed = time.time() - start_time
    
    # Generate summary
    print(f"\n{'='*60}")
    print(" TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Total Repositories: {len(REPOSITORIES)}")
    print(f"Successful: {sum(1 for r in results if r['success'])}")
    print(f"Failed: {sum(1 for r in results if not r['success'])}")
    print(f"Time: {elapsed:.2f} seconds")
    
    # Save results
    summary_file = Path("test_summary.json")
    summary_file.write_text(json.dumps({
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total": len(REPOSITORIES),
        "successful": sum(1 for r in results if r['success']),
        "results": results
    }, indent=2))
    print(f"\n Summary saved to: {summary_file}")

if __name__ == "__main__":
    main()