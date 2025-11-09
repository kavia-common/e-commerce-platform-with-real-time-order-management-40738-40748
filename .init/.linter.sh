#!/bin/bash
cd /home/kavia/workspace/code-generation/e-commerce-platform-with-real-time-order-management-40738-40748/ecommerce_backend
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

