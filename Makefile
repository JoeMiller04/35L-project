.PHONY: deps load-db check clean

deps:
	pip install -r server/requirements.txt

load-db: deps
# This will reset your course database
	python server/data/uclagrades/process21f-22s.py server/data/uclagrades/grades-21f-222.csv
	python server/data/uclagrades/process22f-23s.py server/data/uclagrades/grades-22f-23s.csv
	python server/data/uclagrades/process23f-24s.py server/data/uclagrades/grades-23f-24s.csv
	echo "Grades database loaded successfully."
# This will reset your course descriptions database
	python server/data/Kyle/load_descriptions.py server/data/Kyle/35L-project.descriptions.json --drop

setup-env:
	@if [ ! -f server/.env ]; then \
        echo "Creating default .env file"; \
        echo 'ADMIN_KEY=abc' > server/.env; \
		echo "PLEASE CHANGE THIS KEY"; \
	else \
		echo ".env file already exists"; \
    fi

check: deps setup-env
	pytest

clean: deps
	echo "Removing all example courses from database"