#!/bin/sh

which py.test || exit 1
(
cd $(git rev-parse --show-toplevel)
find src -name '*.pyc' -delete
py.test -v src || exit 1
python setup.py check -r || exit 1
)
