.PHONY: bootstrap clean update runserver

VENV=.venv
PYTHON=$(VENV)/bin/python3
SRC_DIR=./social_network

bootstrap: $(VENV)/bin/activate
$(VENV)/bin/activate:
	python3 -m venv $(VENV)
	$(PYTHON) -m pip install -r requirements.txt

clean: bootstrap
	rm -r .venv

update:
	$(PYTHON) -m pip install -U -r requirements.txt

runserver:
	$(PYTHON) $(SRC_DIR)/manage.py runserver

shell:
	$(PYTHON) $(SRC_DIR)/manage.py shell
