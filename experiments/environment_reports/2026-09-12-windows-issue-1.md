# M0 Environment Verification

## Context

- Date: 2026-09-12
- Knowledge tag or unreleased status: v0.1.0
- Knowledge commit, full SHA: 88a4deb04e2e48bff0e465e784e285c8c5f13591
- Work commit, full SHA: dd403990421542531c0aad2d1239760359ddea3ad
- Related Issue or personal progress entry: #1 Record M0 environment verification
- Operating system: Windows
- Shell: Git Bash

## Environment

- Conda version: 26.7.1
- Environment name used for this run: robot_manipulation_learning
- Python version: 3.11.16
- NumPy version: 2.4.6
- pytest version: 8.4.2

## Commands and results

```bash
python examples/hello_robot.py
python -m pytest
```
Results:
- `hello_robot.py` ran successfully.
- Output included `Hello Robot`.
- Python version: 3.11.16
- NumPy version: 2.4.6
- Project root resolved to the local `practice` repository.
- pytest collected 2 tests.
- Result: `2 passed in 0.11s`.


## Problems and resolution

None observed

## Privacy check

- [x] No host name, user name or student ID
- [x] No private absolute path or IP address
- [x] No token, password or other credential
- [x] Results came from actual execution
