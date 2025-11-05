#!/bin/bash
cd /home/kavia/workspace/code-generation/employee-efficiency-analysis-platform-217538-217576/employee_efficiency_backend
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

