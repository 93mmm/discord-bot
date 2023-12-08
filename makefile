install:
		pip3 install -r requirements.txt
		
run:
		python3 main.py

env:
		python3 -m venv venv
		source venv/bin/activate
