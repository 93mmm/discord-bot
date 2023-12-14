ifeq ($(OS), Windows_NT)
	PYTHON_PIP = pip
	PYTHON     = python
else
	PYTHON_PIP = pip3
	PYTHON     = python3
endif

install:
	sh venv/bin/activate && $(PYTHON_PIP) install -r requirements.txt

run:
	sh venv/bin/activate && $(PYTHON) src/main.py

env:
	$(PYTHON) -m venv venv

