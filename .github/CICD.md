# CI/CD Documentation

## Overview

This project uses GitHub Actions to automatically run tests and quality checks on every push and pull request.

## Workflows

### Tests Workflow (`.github/workflows/tests.yml`)

Runs automated tests across multiple Python versions to ensure compatibility and code quality.

#### Test Job

**Matrix Strategy:**
- Operating System: Ubuntu Latest
- Python Versions: 3.9, 3.10, 3.11, 3.12

**Steps:**
1. **Checkout Code**: Uses `actions/checkout@v4` to get the latest code
2. **Setup Python**: Uses `actions/setup-python@v5` with pip caching for faster builds
3. **Install Dependencies**: Installs package with dev dependencies (`pip install -e ".[dev]"`)
4. **Run Tests**: Executes pytest with coverage reporting
   - Target: 70%+ coverage (enforced with `--cov-fail-under=70`)
   - Formats: XML, HTML, and terminal output
5. **Upload to Codecov** (Python 3.11 only): Optional coverage tracking
6. **Upload HTML Artifact** (Python 3.11 only): Stores coverage report for 30 days

#### Lint Job

Runs code quality checks independently from tests.

**Checks:**
- **Black**: Code formatting (`black --check`)
- **isort**: Import sorting (`isort --check-only`)
- **flake8**: Code linting (max line length 100)

## Test Coverage

Current coverage: **70.23%** (exceeds 70% requirement)

**Coverage Breakdown:**
- `document_generator.py`: 92%
- `accuracy_evaluator.py`: 96%
- `metrics.py`: 100%
- `plotter.py`: 65%
- `base_experiment.py`: 95%
- `exp1_needle_haystack.py`: 100%
- `exp2_context_size.py`: 100%
- `exp3_rag_impact.py`: 100%
- `exp4_context_strategies.py`: 100%

## Triggers

The workflow runs on:
- **Push** to `main` or `develop` branches
- **Pull Requests** targeting `main` or `develop` branches

## Artifacts

### Coverage Reports

After each workflow run on Python 3.11:

1. **HTML Report** (Artifact)
   - Available in Actions tab → Workflow run → Artifacts
   - Download and extract to view detailed coverage
   - Retention: 30 days

2. **Codecov Upload** (Optional)
   - Requires `CODECOV_TOKEN` secret to be configured
   - Provides online coverage tracking and PR comments
   - Set to `fail_ci_if_error: false` so CI doesn't fail without token

## Local Testing

Before pushing, run the same checks locally:

```bash
# Run tests with coverage (same as CI)
pytest tests/ \
  --cov=src/context_windows_lab \
  --cov-report=term-missing \
  --cov-report=html \
  --cov-fail-under=70 \
  -v

# Check code formatting
black --check src/ tests/

# Check import sorting
isort --check-only src/ tests/

# Run linter
flake8 src/ tests/ --max-line-length=100
```

## Troubleshooting

### Failed Tests

If tests fail in CI:
1. Check the workflow run logs in the Actions tab
2. Reproduce locally with the same Python version
3. Fix the failing tests
4. Push the fix

### Coverage Below 70%

If coverage drops below 70%:
1. Add tests for uncovered code
2. Check coverage report: `open htmlcov/index.html`
3. Focus on untested functions/branches
4. Push updated tests

### Linting Failures

If Black/isort/flake8 fails:
1. Run formatters locally: `black src/ tests/`
2. Fix import order: `isort src/ tests/`
3. Fix flake8 issues manually
4. Commit and push

## Future Enhancements

Potential improvements:
- [ ] Add mypy type checking to CI
- [ ] Add security scanning (bandit, safety)
- [ ] Add dependency vulnerability checks
- [ ] Add performance benchmarking
- [ ] Add deployment workflow
- [ ] Add release automation
- [ ] Integration with code quality services (CodeClimate, SonarCloud)

## Badges

Add to README:

```markdown
[![Tests](https://github.com/LiorLivyatan/HW5_RAG_Context_Window/actions/workflows/tests.yml/badge.svg)](https://github.com/LiorLivyatan/HW5_RAG_Context_Window/actions/workflows/tests.yml)
[![Coverage](https://img.shields.io/badge/coverage-70%25-brightgreen.svg)](https://github.com/LiorLivyatan/HW5_RAG_Context_Window)
```

## Status

✅ **All checks passing**
- 86 tests across 12 test files
- Python 3.9, 3.10, 3.11, 3.12 compatibility
- 70.23% code coverage
- Black/isort/flake8 compliant
