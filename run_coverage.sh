#!/bin/bash
#
# Coverage Generation Script for Context Windows Lab
# This script runs pytest with coverage and generates HTML reports
#

set -e  # Exit on error

echo "=================================================="
echo "Context Windows Lab - Test Coverage Report"
echo "=================================================="
echo ""

# Colors for output
GREEN='\033[0.32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if venv is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo -e "${YELLOW}Warning: No virtual environment detected.${NC}"
    echo "Activating test_venv..."
    source test_venv/bin/activate
fi

echo -e "${BLUE}Step 1: Running tests with coverage...${NC}"
pytest --cov=src/context_windows_lab \
       --cov-report=html \
       --cov-report=term-missing \
       --cov-report=xml \
       --cov-fail-under=70 \
       -v

echo ""
echo -e "${BLUE}Step 2: Copying coverage reports to docs...${NC}"
mkdir -p docs/test_coverage
cp -r htmlcov/* docs/test_coverage/ 2>/dev/null || true
cp coverage.xml docs/test_coverage/ 2>/dev/null || true

echo ""
echo -e "${GREEN}✅ Coverage report generated successfully!${NC}"
echo ""
echo "📊 Coverage Reports Available:"
echo "  - HTML: htmlcov/index.html"
echo "  - HTML (docs): docs/test_coverage/index.html"
echo "  - XML: coverage.xml"
echo ""
echo "To view HTML report:"
echo "  open htmlcov/index.html"
echo ""
echo "To view in browser:"
echo "  python3 -m http.server 8000 --directory htmlcov"
echo "  Then open: http://localhost:8000"
echo ""
