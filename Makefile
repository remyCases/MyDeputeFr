PYTHON=python
ifeq ($(OS),Windows_NT)
  VENV=.venv
  BIN=$(VENV)\Scripts
  PIP=$(BIN)\pip
  PYTEST=$(BIN)\pytest
  MYPY=$(BIN)\mypy
else
  VENV=venv
  BIN=$(VENV)/bin
  PIP=$(BIN)/pip
  PYTEST=$(BIN)/pytest
  MYPY=$(BIN)/mypy
endif

# install
install_venv:
	$(PYTHON) -m venv --clear $(VENV)
	$(BIN)\$(PYTHON) -m pip install --upgrade pip

install: install_venv
	$(PIP) install --upgrade -r ./requirements.txt

install_dev: install_venv
	$(PIP) install --upgrade -r ./requirements-dev.txt

# unit testing
test:
	$(PYTEST) -v

# type annotations
mypy:
	$(MYPY) . --strict

# unit testing + type checking
check: test mypy