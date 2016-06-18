#!/bin/bash
# set -ev
set -v

# don't run coverage with pypy

rm -f .coverage
cd test
coverage run --source=rhea -m pytest --durations=10
mv .coverage ../.coverage.mn

cd ../examples
coverage run --source=rhea -m pytest --durations=10
mv .coverage ../.coverage.ex

cd ..
coverage combine

