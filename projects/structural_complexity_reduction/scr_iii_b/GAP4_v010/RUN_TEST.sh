#!/bin/sh
set -eu
cd "$(dirname "$0")"
g++ -std=c++17 -O2 -Wall -Wextra solver_v010.cpp -o solver_v010
python3 test_v010.py
