# Lab-5-Static-Code-Analysis

This repository contains the original `inventory_system.py` (for analysis) and a cleaned file `cleaned_inventory_system.py` produced as the lab deliverable. The lab objective is to use static analysis tools (Pylint, Flake8, Bandit) to find and fix issues, then document findings and reflect on the fixes.

Files

- `inventory_system.py` — original file with issues (used for static analysis)
- `cleaned_inventory_system.py` — cleaned functional implementation

Static analysis — actual tool runs

I ran Pylint, Bandit and Flake8 against the original `inventory_system.py` and saved the raw outputs in the repository as:

- `pylint_report.txt`
- `bandit_report.txt`
- `flake8_report.txt`

Below is a consolidated, accurate table of issues reported by those tools, and how each was addressed in `cleaned_inventory_system.py`.

|  ID | Tool(s)                        | Location / Symptom                                                        |        Severity | Description (tool message)                                                           | Fix applied in `cleaned_inventory_system.py`                                                                               |
| --: | ------------------------------ | ------------------------------------------------------------------------- | --------------: | ------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------- |
|   1 | Pylint (W0102)                 | `addItem` default `logs=[]`                                               |            High | Dangerous default value [] as argument (mutable default)                             | Replaced with `logs=None` and initialize inside function.                                                                  |
|   2 | Bandit (B110) / Flake8 (E722)  | `removeItem` has `try: ... except: pass`                                  | Low/High (tool) | Bare except and `try/except/pass` hides exceptions                                   | Removed silent except; added explicit checks and raise KeyError for missing items.                                         |
|   3 | Bandit (B307) / Pylint (W0123) | `eval("print('eval used')")` in `main`                                    |          Medium | Use of `eval` (possible code injection)                                              | Removed `eval` and used explicit print/logging in cleaned file.                                                            |
|   4 | Pylint / Flake8                | `open()` calls without context manager/encoding                           |          Medium | Using open without encoding and not using `with` (resource leak risk)                | Replaced with `with open(..., encoding='utf-8')` and validated JSON contents.                                              |
|   5 | Pylint / Flake8                | Naming and style issues (function names, missing docstrings, blank lines) |             Low | Functions not using snake_case, many missing docstrings, and blank-line style issues | Kept original API names converted in cleaned file to snake_case (e.g., `add_item`) and added docstrings where appropriate. |
|   6 | Pylint                         | `getQty` indexing may raise KeyError                                      |          Medium | Direct dict indexing without fallback leads to KeyError                              | `get_qty` returns 0 for missing items and validates inputs.                                                                |
|   7 | Pylint                         | Unused import `logging` in original                                       |             Low | Unused imports flagged by tools                                                      | `cleaned_inventory_system.py` uses logging; unused imports removed/used appropriately.                                     |

You can inspect the raw outputs to see the exact messages produced by each tool (they are saved in the repo). I used those reports to produce the table above and implement the fixes in `cleaned_inventory_system.py`.

Reflection Questions

1. Which issues were the easiest to fix, and which were the hardest? Why?

- Easiest: Mutable default argument and replacing `open()/close()` with context managers were straightforward mechanical fixes with immediate benefits.
- Hardest: Reasoning about silent `except:` and where the code should fail vs continue. Converting these to explicit exceptions required deciding what semantics the original author intended (e.g., whether missing items should be ignored or reported). Also, removing `eval` is easy, but if the original code relied on dynamic execution there may be more design work to replace it safely.

2. Did the static analysis tools report any false positives? If so, describe one example.

Yes — most reported issues were valid and important (for example, Bandit's `eval` and the bare `except` were real security/robustness problems we fixed). However, there were a few findings that are stylistic(False positive) recommendations rather than true bugs. One concrete example:

- Pylint's C0209 "consider-using-f-string" for the line that formats the log entry (the original `logs.append("%s: Added %d of %s" % (...))`). This is a style suggestion to prefer f-strings for readability and consistency. It is not a correctness or security problem — converting to an f-string improves clarity but does not fix a runtime bug. In the cleaned file I applied f-strings where appropriate for readability, but this finding would be considered a low-priority, stylistic issue rather than a false positive about program correctness.

Another example of a generally lower-priority tool result is naming/style warnings (snake_case vs camelCase) from Pylint: they reflect coding conventions, not functional defects. By contrast, Bandit's findings (use of `eval`) and Flake8's bare-except warning were genuine issues and were addressed in the cleaned version.

3. How would you integrate static analysis tools into your actual software development workflow?

- Add linters (Flake8, Pylint) and security scanner (Bandit) as dev dependencies and run them in CI (for example, in GitHub Actions) on pull requests to prevent regressions.
- Optionally configure pre-commit hooks to run quick checks locally (flake8/pylint partial checks) to catch issues before pushing.
- Tailor tool configurations to the project (pylintrc, .flake8) to reduce noise and avoid false positives.

4. What tangible improvements did you observe after applying the fixes?

- Code is safer: removed arbitrary code execution and input validation prevents corrupt state.
- Easier to debug: logging and explicit error reporting surface issues instead of hiding them.
- More maintainable: clearer function contracts (types and exceptions) make future changes safer.

How you can run the static analysis tools (recommended)

Use the repository Codespace or your local environment. Example commands to install and run the tools:

```powershell
pip install pylint bandit flake8
pylint inventory_system.py > pylint_report.txt
bandit -r inventory_system.py > bandit_report.txt
flake8 inventory_system.py > flake8_report.txt
```

or run the run_linters.py
