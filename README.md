# Codebase Sanity Checker (CSC)
An agentic workflow for automated codebase health assessment.

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)

##  Table of Contents
- [Problem Statement](#problem-statement)
- [Who Has This Problem?](#who-has-this-problem)
- [Solution Overview](#solution-overview)
- [Baseline vs Advanced](#baseline-vs-advanced)
- [Installation](#installation)
- [Usage](#usage)
- [Evaluation Results](#evaluation-results)
- [Improvement Changelog](#improvement-changelog)
- [Video Demo](#video-demo)
- [Reproduction Guide](#reproduction-guide)
- [Technical Architecture](#technical-architecture)
- [Future Work](#future-work)

## Problem Statement
### Who Has This Problem?
Software engineers and team leads need to quickly understand the health,structure, and risks of unfamiliar codebases.

### What Bottleneck Makes It Worth Solving?
- **Time-consuming**: Manually reviewing a complex repository takes hours or days
- **Inconsistent**: Different reviewers reach different conclusions
- **Incomplete**: Easy to miss critical issues like failing tests or outdated dependencies
- **No standard metric**: No objective way to compare codebase quality

### Why Solve It?
- **Faster onboarding**: New team members understand codebase quality quickly
- **Better decisions**: Make informed decisions about code acquisition or refactoring
- **Objective metrics**: Quantify code quality with a standardized score (0-100)
- **Actionable insights**: Get specific recommendations for improvement


##  Solution Overview

The Codebase Sanity Checker is an **agentic workflow** that:
1. **Clones** any public GitHub repository
2. **Analyzes** repository structure and complexity
3. **Runs** tests and linting (pytest, flake8)
4. **Checks** dependencies (requirements.txt, setup.py, pyproject.toml)
5. **Scores** code quality (0-100 with breakdowns)
6. **Recommends** actionable improvements
7. **Generates** professional reports (Markdown + JSON)

##  Baseline vs Advanced

### Baseline Approach
- Simple script running `pytest` and `flake8`
- Raw output only (pass/fail, issue counts)
- No scoring or analysis
- No structured recommendations

### Advanced Agentic Solution
- **Multi-agent workflow** (Analyzer, Verifier, Extractor, Reviewer)
- **Comprehensive scoring** with breakdowns (Tests, Linting, Structure, Dependencies)
- **Actionable recommendations** tailored to findings
- **Professional reports** with clear metrics
- **JSON output** for data analysis

### Comparison Table

| Feature | Baseline | Advanced |
|---------|----------|----------|
| Repository Analysis | ❌ | ✅ |
| Test Execution | ✅ | ✅ |
| Linting | ✅ | ✅ |
| Dependency Check | ❌ | ✅ |
| Quality Score | ❌ | ✅ |
| Breakdown Analysis | ❌ | ✅ |
| Recommendations | ❌ | ✅ |
| Professional Report | ❌ | ✅ |
| JSON Export | ❌ | ✅ |

##  Installation

### Prerequisites
- Python 3.8 or higher
- Git
- pip

## Quick start
```bash
# Clone the repository
git clone https://github.com/Nausheenkhan-git/codebase-sanity-checker.git
cd codebase-sanity-checker

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the checker
python run.py --repo https://github.com/psf/requests.git 
```
## Usage

### Basic Usage
```bash
# Analyze a GitHub repository (Baseline mode)
python run.py --repo https://github.com/psf/requests.git

# Save report to a specific directory
python run.py --repo https://github.com/psf/requests.git --output ./reports

# Advanced analysis mode
python run.py --repo https://github.com/psf/requests.git --advanced
```
### Batch Testing
```bash
# Test multiple repositories
python test_repos.py

# Or use the provided script
./test_repos.sh
```

## Output
The system generates:

- Markdown Report (./reports/report_YYYYMMDD_HHMMSS.md)
- JSON Results (latest_results.json)
- Console Output with real-time progress

#  Evaluation Results

## Test Repositories

| Repository | Score | Tests | Linting | Dependencies |
| :--- | :---: | :---: | :---: | :---: |
| **requests** | 40/100 | Failed | 89 issues | 0 |
| **python-guide** | 50/100 | Failed | 44 issues | 20 |
| **flask** | - | - | - | - |

> **Note:** Run the tool on any repository to get results!

---

##  Key Findings

* **Test coverage** varies greatly between repositories.
* **Linting issues** are common even in well-maintained projects.
* **Dependency management** is often inconsistent.
* **Score breakdowns** help identify specific areas for improvement.

---

##  Improvement Changelog

### Baseline
* **What we tried:** Simple script that clones a repo and runs basic checks (`pytest` and `flake8`).
* **Result:** Basic test pass/fail and linting count only.
* **Evidence:** Raw outputs with no structure or scoring.
* **Decision:** Established baseline for comparison.

### Iteration 1
* **What we tried:** Added structured analysis of repository (file count, directory structure, Python files).
* **Result:** Repository overview with metrics.
* **Evidence:** Now shows *"37 Python files, 4 directories"*, etc.
* **Decision:** Kept — provides valuable context about codebase size.

### Iteration 2
* **What we tried:** Added comprehensive scoring system (0–100) with breakdowns.
* **Result:** Quantifiable quality score with detailed components.
* **Evidence:** `Score: 40/100 (Tests: 10/30, Linting: 5/30, Structure: 20/20, Dependencies: 5/20)`
* **Decision:** Kept — makes comparison objective and clear.

### Iteration 3
* **What we tried:** Added dependency analysis (`requirements.txt`, `setup.py`, `pyproject.toml`).
* **Result:** Can identify missing dependency management.
* **Evidence:** Found `pyproject.toml` and `setup.py` but no `requirements.txt`.
* **Decision:** Kept — helps assess project maturity.

### Iteration 4
* **What we tried:** Added actionable recommendations based on findings.
* **Result:** Clear next steps for improvement rather than just raw data.
* **Evidence:** *"Fix failing tests"*, *"Fix linting issues"*, *"Add requirements.txt"*
* **Decision:** Kept — increases practical value for users.

### Iteration 5
* **What we tried:** Added JSON output and report generation.
* **Result:** Structured data for analysis and professional markdown reports.
* **Evidence:** `latest_results.json` and `report_*.md` files generated.
* **Decision:** Kept — enables tracking over time.

### Final
* **What we tried:** Combined all features into complete workflow.
* **Result:** Comprehensive report with score, structure, tests, linting, dependencies, and recommendations.
* **Evidence:** Full report shown above with all metrics.

**Main Contribution:** Automated codebase health assessment with actionable insights.

## Reproduction guide

### Setup from Clean Environment
```bash
# 1. Clone repository
git clone https://github.com/Nausheenkhan-git/codebase-sanity-checker.git
cd codebase-sanity-checker

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the checker (solution)
python run.py --repo https://github.com/psf/requests.git

# 5. Run baseline comparison
python run.py --repo https://github.com/psf/requests.git --baseline

# 6. Save report
python run.py --repo https://github.com/psf/requests.git --output ./reports
```

### Expected Output
```bash
============================================================
CODEBASE SANITY CHECKER
============================================================
Repository: https://github.com/psf/requests.git
Mode: Baseline
------------------------------------------------------------
Cloning https://github.com/psf/requests.git...
Analyzing repository structure...
Running tests...
Running linters...
```

### Runtime & Cost 
- Runtime: ~30-120 seconds per repository
- Cost: $0 all open-source tools
- Disk Space: ~100-500MB per repository(cleaned up automatically)

##  Project Structure

```text
Codebase Sanity Checker
├── run.py                          # Main orchestrator
├── functions/
│   ├── clone_repo()                # Git operations
│   ├── analyze_structure()         # File/directory analysis
│   ├── run_tests()                 # pytest execution
│   ├── run_linting()               # flake8 execution
│   ├── check_dependencies()        # requirements analysis
│   ├── generate_report()           # Markdown report
│   ├── calculate_score()           # 0-100 scoring
│   └── generate_recommendations()  # Actionable insights
├── outputs/
│   ├── reports/*.md                # Markdown reports
│   └── latest_results.json         # JSON data
└── requirements.txt                # Python dependencies
```

## Future Work

- OpenAI integration for deeper analysis
- Multi-language support (JavaScript, Java, Go, Rust)
- Historical trend analysis
- Web dashboard for visualization
- CI/CD integration
- Custom score weighting
- Security vulnerability scanning
- Code complexity metrics

## Contributing
Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Acknowledgments
- Built for the micro1 Agentic Workflows Hackathon
- Inspired by real-world code review challenges
- Built with Python, pytest, flake8, and Git