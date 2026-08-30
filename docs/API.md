\# API Documentation



\## Core Functions



\### clone\_repo(repo\_url)

Clones a GitHub repository to a temporary directory.



\*\*Parameters:\*\*

\- `repo\_url` (str): GitHub repository URL



\*\*Returns:\*\*

\- `Path`: Path to cloned repository, or None if failed



\### analyze\_structure(repo\_path)

Analyzes repository structure and returns metrics.



\*\*Parameters:\*\*

\- `repo\_path` (Path): Path to repository



\*\*Returns:\*\*

\- `dict`: Structure analysis with files, directories, Python files



\### run\_tests(repo\_path)

Runs pytest tests if available.



\*\*Parameters:\*\*

\- `repo\_path` (Path): Path to repository



\*\*Returns:\*\*

\- `dict`: Test results with status, output, errors



\### run\_linting(repo\_path)

Runs flake8 linting if available.



\*\*Parameters:\*\*

\- `repo\_path` (Path): Path to repository



\*\*Returns:\*\*

\- `dict`: Linting results with issues and count



\### check\_dependencies(repo\_path)

Checks Python dependencies.



\*\*Parameters:\*\*

\- `repo\_path` (Path): Path to repository



\*\*Returns:\*\*

\- `dict`: Dependencies with count and file indicators



\### generate\_report(results)

Generates a markdown report.



\*\*Parameters:\*\*

\- `results` (dict): Analysis results



\*\*Returns:\*\*

\- `str`: Markdown report



\### calculate\_score(results)

Calculates quality score (0-100).



\*\*Parameters:\*\*

\- `results` (dict): Analysis results



\*\*Returns:\*\*

\- `int`: Quality score



\### generate\_recommendations(results)

Generates actionable recommendations.



\*\*Parameters:\*\*

\- `results` (dict): Analysis results



\*\*Returns:\*\*

\- `str`: Formatted recommendations



\## Output Format



\### JSON Output

```json

{

&#x20; "repo\_url": "https://github.com/psf/requests.git",

&#x20; "mode": "baseline",

&#x20; "structure": {...},

&#x20; "tests": {...},

&#x20; "linting": {...},

&#x20; "dependencies": {...}

}

