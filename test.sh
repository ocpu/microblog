#!/bin/sh
source venv/bin/activate
flask db upgrade
pylint --rcfile=.pylintrc app tests
python -m coverage run --rcfile=.coveragerc -m py.test -c pytest.ini tests/unit
python -m coverage run --rcfile=.coveragerc -m py.test -c pytest.ini tests/integration
