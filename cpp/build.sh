#!/usr/bin/env bash
set -euo pipefail

CXX=${CXX:-g++}
STD=${STD:-c++17}
OUT=${OUT:-demo}
LIBNAME=${LIBNAME:-mylib}

command -v "$CXX" >/dev/null || {
  echo "error: compiler $CXX not found" >&2; exit 1; }

[[ -f demo.cpp && -f mylib.cpp && -f mylib.hpp ]] || {
  echo "error: missing demo.cpp/mylib.cpp/mylib.hpp" >&2; exit 1; }

"$CXX" -std="$STD" -O2 -Wall -Wextra -pedantic -c mylib.cpp -o mylib.o

ar rcs "lib${LIBNAME}.a" mylib.o

"$CXX" -std="$STD" -O2 -Wall -Wextra -pedantic demo.cpp "./lib${LIBNAME}.a" -o "$OUT"

./"$OUT"
