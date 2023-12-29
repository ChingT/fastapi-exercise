#! /usr/bin/env bash
set -e

python -m app.tests_pre_start

bash app/scripts/test.sh "$@"
