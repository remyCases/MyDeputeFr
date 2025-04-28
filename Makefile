PYTHON=python
ifeq ($(OS),Windows_NT)
  VENV=.venv
  BIN=$(VENV)\Scripts
  PIP=$(BIN)\pip
  PYTEST=$(BIN)\pytest
else
  VENV=venv
  BIN=$(VENV)/bin
  PIP=$(BIN)/pip
  PYTEST=$(BIN)/pytest
endif

# install
install_venv:
	$(PYTHON) -m venv --clear $(VENV)

install: install_venv
	$(PIP) install --upgrade -r ./requirements.txt

install_dev: install_venv
	$(PIP) install --upgrade -r ./requirements-dev.txt

# test
test:
	$(PYTEST) -v
