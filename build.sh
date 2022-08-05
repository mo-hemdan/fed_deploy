#!/bin/sh
rm dist/*
python3 -m build
yes $'__token__' | python3 -m twine upload --repository testpypi dist/*
pip uninstall fed_deploy
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps fed_deploy