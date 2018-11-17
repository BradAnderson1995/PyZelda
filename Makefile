PYTHON=python2.7

ENV_DIR=.env_$(PYTHON)

ifeq ($(OS),Windows_NT)
	IN_ENV=. $(ENV_DIR)/Scripts/activate &&
else
	IN_ENV=. $(ENV_DIR)/bin/activate &&
endif

all: test lint artifacts

env: $(ENV_DIR)


artifacts: build_reqs sdist

$(ENV_DIR):
	virtualenv -p $(PYTHON) $(ENV_DIR)

build_reqs: env
	$(IN_ENV) pip install unify

build: build_reqs
	$(IN_ENV) pip install --editable .

sdist: build_reqs
	$(IN_ENV) python setup.py sdist

lint: pep8

pep8: build_reqs
	- $(IN_ENV) pep8 src/doc_manager > pep8.out

freeze: env
	- $(IN_ENV) pip freeze

shell:
	- $(IN_ENV) python

run: build
	- $(IN_ENV) zelda

unify: build_reqs
	- $(IN_ENV) unify --in-place --recursive src/

clean:
	- @rm -rf BUILD
	- @rm -rf BUILDROOT
	- @rm -rf RPMS
	- @rm -rf SRPMS
	- @rm -rf SOURCES
	- @rm -rf docs/build
	- @rm -rf src/*.egg-info
	- @rm -rf build
	- @rm -rf dist
	- @rm -f .coverage
	- @rm -f test_results.xml
	- @rm -f tests/coverage.xml
	- @rm -f coverage.xml
	- @rm -f pep8.out
	- @find . -name '*.pyc' -delete
	- @find . -name '*.pyo' -delete
	- @find . -name '*.pyd' -delete
	- @find . -name '*__pycache__' -delete

env_clean: clean
	- @rm -rf .env*
	- @rm -rf $(ENV_DIR)
