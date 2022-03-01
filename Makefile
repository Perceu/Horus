entrypoint=app.py
pythonpath=.venv/bin/python
pippath=.venv/bin/pip

setup:
	@echo "\nSetting up workspace..."
	
	sudo apt-get install\
		python3\
		python3-venv\
		python3-dev\
		build-essential\
		-y

	@echo "\nCreating python virtual environment"
	python3 -m venv .venv

	@echo "\nInstalling python packages"

	$(pippath) install -r requirements.txt

	@echo "\nDone!"	

run:
	$(pythonpath) $(entrypoint) 
