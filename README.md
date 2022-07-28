# pyhub

Write github actions with python.

[test.py](test.py) contains all possible config options currently

when you run `python test.py` it generates [workflow.yaml](workflow.yaml) which you could commit to your repo and run in actions

This is a WIP this readme would need lots of cleaning.

# Install
1. python3 -m pip install git+ssh://git@github.com/Apollorion/pyhub.git

Now you can use `pyhub`!

# Dev

### Install
1. clone this repo
2. cd pyhub
3. python -m pip install --editable .

### Tests
`./run_unit_tests.sh`