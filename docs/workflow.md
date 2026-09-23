# Detailed Workflow

This document records the working process used in this repository.

The purpose of the workflow is to keep learning, implementation, testing, documentation, and Git history organized and reproducible.

## 1. Start a Work Session

Open Git Bash and enter the practice repository:

```bash
cd ~/robot-learning/practice
```

Activate the Conda environment:

```bash
conda activate robot_manipulation_learning
```

Check the current repository state:

```bash
git status
```

Before starting new work, make sure the working tree is in the expected state.

---

## 2. Create a Branch for Substantial Changes

For a meaningful new task, create a dedicated branch from the latest `main`.

First update `main`:

```bash
git switch main
git pull
```

Then create a new branch:

```bash
git switch -c <branch-name>
```

Example:

```bash
git switch -c docs/m1-final-completion
```

Small corrections may occasionally be made directly on `main`, but feature branches are preferred for substantial work.

---

## 3. Learn the Concept First

Before implementing a robotics concept:

1. understand the mathematical or programming idea
2. work through a small example
3. identify input and output shapes
4. understand the coordinate-frame meaning where relevant
5. connect the formula with the corresponding NumPy operation

For robotics mathematics, special attention should be paid to frame conventions and matrix multiplication order.

---

## 4. Implement a Small, Testable Unit

Implementation should be divided into small functions whenever possible.

Typical locations include:

```text
algorithms/
examples/
```

Before writing a large amount of code, first make sure the smallest meaningful function works correctly.

Important checks may include:

- expected input shape
- expected output shape
- finite numeric values
- correct matrix dimensions
- correct coordinate-frame semantics
- no unexpected input mutation

---

## 5. Add Tests

Tests are stored under:

```text
tests/
```

Testing should cover more than only the normal example.

Where appropriate, include:

- expected numerical results
- shape checks
- invalid input checks
- non-finite values
- empty inputs
- round-trip checks
- mathematical invariants

Examples of useful robotics checks include:

```text
R.T @ R ≈ I
det(R) ≈ 1
```

and:

```text
T_inv @ T ≈ I
```

---

## 6. Run Tests During Development

For a specific test file:

```bash
python -m pytest tests/<test_file>.py
```

For the full repository:

```bash
python -m pytest
```

A task should not be considered complete only because the example code runs once.

The relevant tests should also pass.

---

## 7. Record Learning Notes

Concept notes are stored under:

```text
notes/
```

Notes should explain the ideas in a way that can be reviewed later.

Where useful, notes may include:

- definitions
- formulas
- intuitive explanations
- small numerical examples
- NumPy representations
- common mistakes
- links between mathematics and implementation

English and Chinese notes may both be maintained when useful.

---

## 8. Record Experiments

Experiment records are stored under:

```text
experiments/
```

An experiment record should describe, when relevant:

- purpose
- environment
- implementation
- test result
- observed behavior
- debugging process
- conclusion
- limitations

The goal is to preserve not only successful results, but also useful reasoning and debugging evidence.

---

## 9. Update Progress Records

After completing a meaningful learning stage, update:

```text
progress.md
```

and the relevant README files.

The documentation should reflect the actual repository state.

A module should only be marked as completed after its required learning, implementation, testing, experiments, and documentation have been finished.

---

## 10. Review Changes Before Committing

Check the repository:

```bash
git status
```

Inspect changes:

```bash
git diff
```

After staging:

```bash
git diff --staged
```

Make sure unrelated files are not accidentally included.

---

## 11. Stage and Commit

Stage the intended files:

```bash
git add <files>
```

Create a clear commit:

```bash
git commit -m "<commit message>"
```

Commit messages should briefly describe the purpose of the change.

Examples:

```text
docs: complete M1 robot math foundations
feat: add rigid transform utilities
test: expand transform validation coverage
```

---

## 12. Push and Open a Pull Request

Push the branch:

```bash
git push -u origin <branch-name>
```

Then create a pull request on GitHub.

Before merging, verify:

- the intended files are included
- the documentation renders correctly
- the test suite passes
- no unrelated changes are present

After review, merge the pull request into `main`.

---

## 13. Synchronize Local Main

After the pull request has been merged:

```bash
git switch main
git pull
git status
```

The final expected state is:

```text
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

---

## Workflow Summary

The general workflow is:

```text
Learn
  ↓
Understand
  ↓
Implement
  ↓
Test
  ↓
Experiment
  ↓
Document
  ↓
Review
  ↓
Commit
  ↓
Pull Request
  ↓
Merge
  ↓
Synchronize
```

This workflow may evolve as the repository grows, but the main principle remains the same:

> Learn carefully, implement in small steps, verify with tests, and keep the repository history clear and reproducible.