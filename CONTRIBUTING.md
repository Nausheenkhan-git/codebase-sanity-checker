\# Contributing to Codebase Sanity Checker



We love your input! We want to make contributing as easy as possible.



\## Getting Started



1\. Fork the repository

2\. Clone your fork: `git clone https://github.com/your-username/codebase-sanity-checker.git`

3\. Create a branch: `git checkout -b feature/amazing-feature`

4\. Make your changes

5\. Test your changes: `python run.py --repo https://github.com/psf/requests.git`

6\. Commit your changes: `git commit -m 'Add amazing feature'`

7\. Push to the branch: `git push origin feature/amazing-feature`

8\. Open a Pull Request



\## Development Setup



```bash

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

```



\## Code Style



* Follow PEP 8
* Use descriptive variable names
* Add docstrings to functions
* Keep functions focused and small



\## Testing



```bash

\# Test with different repositories

python run.py --repo https://github.com/psf/requests.git

python run.py --repo https://github.com/pallets/flask.git

```



\## Pull Request Process



* Update the README.md with details of changes if needed
* Update the CHANGELOG.md with your changes
* The PR will be merged once reviewed



