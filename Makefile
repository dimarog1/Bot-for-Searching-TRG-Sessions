ifeq ($(shell test -e '.env' && echo -n yes),yes)
    include .env
endif

# parse additional args for commands

args := $(wordlist 2, 100, $(MAKECMDGOALS))
ifndef args
MESSAGE = "No such command (or you pass two or many targets to ). List of possible commands: make help"
else
MESSAGE = "Done"
endif

APPLICATION_NAME = bot

HELP_FUN = \
    %help; while(<>){push@{$$help{$$2//'options'}},[$$1,$$3] \
    if/^([\w-_]+)\s*:.*\#\#(?:@(\w+))?\s(.*)$$/}; \
    print"$$_:\n", map"  $$_->[0]".(" "x(20-length($$_->[0])))."$$_->[1]\n",\
    @{$$help{$$_}},"\n" for keys %help; \


# Commands
env:  ##@Environment Create .env file with variables
	@$(eval SHELL:=/bin/bash)
	@cp .env.example .env

help: ##@Help Show this help
	@echo -e "Usage: make [target] ...\n"
	@perl -e '$(HELP_FUN)' $(MAKEFILE_LIST)

db:  ##@Database Create database with docker-compose
	docker compose -f docker-compose.yaml up bot_db -d --remove-orphans

lint:  ##@Code Check code with pylint
	poetry run python -m pylint $(CODE)

format:  ##@Code Reformat code with isort and black
	poetry run python -m isort $(CODE)
	poetry run python -m black $(CODE)

migrate:  ##@Database Do all migrations in database
	cd $(APPLICATION_NAME)/db && PYTHONPATH=../.. alembic upgrade $(args)

run:  ##@Application Run application server
	poetry run python -m $(APPLICATION_NAME)

revision:  ##@Database Create new revision file automatically with prefix (ex. 2022_01_01_14cs34f_message.py)
	cd $(APPLICATION_NAME)/db && PYTHONPATH=../.. alembic revision --autogenerate

open_db:  ##@Database Open database inside docker-image
	docker exec -it shortener_postgres psql -d $(POSTGRES_DB) -U $(POSTGRES_USER)

clean:  ##@Code Clean directory from garbage files
	rm -fr *.egg-info dist

%::
	echo $(MESSAGE)
