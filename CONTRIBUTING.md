# Contributing

Help us improve EcoLogits Calculator by contributing! :tada:

## Issues

Questions, feature requests and bug reports are all welcome as [discussions or issues](https://github.com/genai-impact/ecologits-calculator/issues/new/choose).

When submitting a feature request or bug report, please provide as much detail as possible. For bug reports, please include relevant information about your environment, including the version of EcoLogits Calculator and other Python dependencies used in your project.

## Pull Requests

Getting started and creating a Pull Request is a straightforward process. Since EcoLogits Calculator is regularly updated, you can expect to see your contributions incorporated into the project within a matter of days or weeks.
For non-trivial changes, please create an issue to discuss your proposal before submitting pull request. This ensures we can review and refine your idea before implementation.

### Prerequisites

You'll need to meet the following requirements:

- **Python version above 3.12**
- **git**
- **[uv](https://docs.astral.sh/uv/getting-started/installation/)**

### Installation and setup

Fork the repository on GitHub and clone your fork locally.

```shell
# Clone your fork and cd into the repo directory
git clone git@github.com:<your username>/ecologits-calculator.git
cd ecologits-calculator

# Install ecologits calculator development dependencies with uv
uv sync
```

### Check out a new branch and make your changes

Create a new branch for your changes.

```shell
# Checkout a new branch and make your changes
git checkout -b my-new-feature-branch
```

### Run tests

Test the calculator locally to make sure everything is working as expected.

### Code formatting and pre-commit

Before pushing your work, run the linter / formatter.

```shell
# Run all checks before commit with Ruff
uv run ruff check .
# Auto-format code with Ruff
uv run ruff format .
```

### Commit and push your changes

Commit your changes, push your branch to GitHub, and create a pull request.

Please follow the pull request template and fill in as much information as possible. Link to any relevant issues and include a description of your changes.

When your pull request is ready for review, add a comment with the message "please review" and we'll take a look as soon as we can.

## Acknowledgment

We'd like to acknowledge that this contribution guide is heavily inspired by the excellent [guide from Pydantic](https://docs.pydantic.dev/latest/contributing/). Thanks for the inspiration! :heart:
