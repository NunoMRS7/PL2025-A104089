#!/bin/bash

mkdir -p out

# Loop through all .pas files in the tests directory
for testfile in tests/*.pas; do
  # Extract the base name without directory and extension
  basename=$(basename "$testfile" .pas)
  
  echo "Running test [$basename]"
  
  # Run the test and redirect output
  cat "$testfile" | python3 main.py > "out/${basename}.vm"
done
