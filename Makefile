PYTHON=python
ifeq ($(OS),Windows_NT)
  BIN=.venv\Scripts
  PIP=$(BIN)\pip
  PYTEST=$(BIN)\pytest
else
  BIN=venv/bin
  PIP=$(BIN)/pip
  PYTEST=$(BIN)/pytest
endif

# install
install_venv:
	$(PYTHON) -m venv --clear .venv
	$(BIN)\$(PYTHON) -m pip install --upgrade pip

install: install_venv
	$(PIP) install --upgrade -r ./requirements.txt

install_dev: install_venv
	$(PIP) install --upgrade -r ./requirements-dev.txt

# test
test:
	$(PYTEST) -v
