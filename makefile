ifeq ($(OS),Windows_NT)
	PYTHON_PIP = pip
	PYTHON     = python
else
	PYTHON_PIP = pip3
	PYTHON     = python3
endif

install:
	$(PYTHON_PIP) install -r requirements.txt

run:
	$(PYTHON) src/main.py

env:
	$(PYTHON) -m venv venv
	source venv/bin/activate