BIN=.venv\Scripts

# install
install_venv:
	python -m venv --clear .venv

install: install_venv
	$(BIN)\pip install --upgrade -r .\requirements.txt

install_dev: install_venv
	$(BIN)\pip install --upgrade -r .\requirements-dev.txt

# test 
test:
	$(BIN)\pytest tests\download -v