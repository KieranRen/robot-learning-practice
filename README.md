# Robot Learning Practice

[English](README.md) | [中文](README_zh.md)

A structured and reproducible record of my robotics learning, implementations, experiments, and technical development.

## About

This repository documents my long-term study of robotics, starting from mathematical and programming foundations and gradually extending toward larger robotics systems.

Each learning module combines:

- theory notes
- independent implementations
- automated tests
- experiments
- reproducible results
- reflections on mistakes and corrections

The goal is not only to complete tutorials, but to build a clear record of what I understand, implement, verify, and improve over time.

## Learning Source

The primary learning material for this repository is maintained in the following upstream repository:

- [noBug01/Robot_knowledge_study](https://github.com/noBug01/Robot_knowledge_study)

This repository does not aim to duplicate the upstream material. Instead, it records my own learning process, including:

- personal notes and summaries
- independent implementations
- tests and numerical verification
- experiment records
- mistakes, corrections, and reflections
- selected extensions and small projects built on top of the learned concepts

The upstream repository is treated as the reference source, while this repository serves as my personal practice, documentation, and development workspace.

When a specific learning task depends on a particular upstream version, the corresponding source version or commit is recorded in the relevant progress or experiment documentation.

## Current Progress

| Module | Topic | Status | Learning Notes | Experiment Evidence |
| --- | --- | --- | --- | --- |
| M0 | Development environment and Git workflow | Completed | — | [Environment Reports](experiments/environment_reports/) |
| M1 | Python, NumPy, coordinate frames, rotations, and rigid-body transformations | In Progress | [M1 Notes](notes/m1/) | [M1 Experiments](experiments/m1/) |

### M1 Highlights

M1 currently includes two completed learning blocks:

#### Python and NumPy Foundations

- array shape, dimensions, and data types
- indexing and slicing
- views and copies
- broadcasting
- vector and matrix operations
- floating-point numerical checks
- automated testing with `pytest`

Learning notes:

- [English](notes/m1/python_numpy.md)
- [中文](notes/m1/python_numpy_zh.md)

Experiment evidence:

- [English](experiments/m1/numeric_basics_report.md)
- [中文](experiments/m1/numeric_basics_report_zh.md)

#### Robot Geometry and Rigid Transforms

- coordinate frames
- rotation matrices
- rigid-body transformations
- homogeneous coordinates
- transform composition
- inverse transforms
- round-trip validation
- coordinate-frame visualization

Learning notes:

- [English](notes/m1/robot_geometry.md)
- [中文](notes/m1/robot_geometry_zh.md)

Experiment evidence:

- [English](experiments/m1/robot_geometry_report.md)
- [中文](experiments/m1/robot_geometry_report_zh.md)

Generated visualization:

- [`outputs/m1/frames.svg`](outputs/m1/frames.svg)

Current automated verification:

```text
Python / NumPy:    22 tests passed
Robot Geometry:    54 tests passed
```

## Repository Structure

```text
robot-learning-practice/
├── notes/          # Personal learning notes and summaries
├── examples/       # Small runnable examples and implementations
├── tests/          # Automated tests
├── experiments/    # Experiment reports and reproducibility evidence
├── docs/           # Roadmap, workflow, and project documentation
├── progress.md     # Ongoing learning progress
├── environment.yml # Reproducible Python environment
└── README.md

## Learning Approach

My learning workflow is based on four steps:

1. Understand the underlying mathematics and concepts.
2. Re-implement the ideas independently.
3. Verify the implementation using tests and numerical checks.
4. Document the reasoning, mistakes, and results for future review.

The purpose of this workflow is to make each topic reproducible, explainable, and useful beyond a single tutorial or exercise.

## Reproducibility

The project uses a Conda environment defined in `environment.yml`.

Typical setup:

```bash
conda env create -f environment.yml
conda activate robot_manipulation_learning
python -m pytest
```

Runnable examples are stored in examples/, while automated checks are stored in tests/.
Where relevant, experiment outputs and environment verification records are stored under experiments/.

## Documentation

- [Learning Notes](notes/README.md)
- [Learning Roadmap](docs/roadmap.md)
- [Detailed Workflow](docs/workflow.md)
- [Progress Record](progress.md)

## Current Focus

I am currently working through M1, with emphasis on:

- Python and NumPy foundations
- array shape, indexing, slicing, and broadcasting
- vector and matrix operations
- numerical precision and floating-point checks
- coordinate frames
- rotation matrices
- rigid-body transformations
- transform composition
- inverse transforms
- automated testing with `pytest`

## Future Directions

Planned areas include:

- robot kinematics
- control systems
- ROS 2
- perception
- SLAM
- manipulation
- simulation
- larger integrated robotics projects

As the repository grows, selected learning modules may be developed into more complete standalone projects with their own documentation, tests, and examples.

"Born in a lab. Built for the future."