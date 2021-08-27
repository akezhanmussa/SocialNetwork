.PHONY: update runserver makemigrations migrate shell clean

VENV=.venv
PYTHON=$(VENV)/bin/python3
SERVER_DIR=./social_network
BOT_DIR=./bot

bootstrap: $(VENV)/bin/activate
$(VENV)/bin/activate:
	python3 -m venv $(VENV)
	$(PYTHON) -m pip install -r requirements.txt

update: bootstrap
	$(PYTHON) -m pip install -U -r requirements.txt

runserver: bootstrap
	$(SERVER_DIR)/manage.py runserver

runbot: bootstrap
	$(PYTHON) $(BOT_DIR)/bot.py

makemigrations: bootstrap
	$(SERVER_DIR)/manage.py makemigrations

migrate: makemigrations
	$(SERVER_DIR)/manage.py migrate

shell: bootstrap
	$(SERVER_DIR)/manage.py shell

clean: bootstrap
	rm -r .venv
