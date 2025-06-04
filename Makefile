.PHONY: deps load-db check clean

deps:
	pip install -r server/requirements.txt

load-db: deps
# This will reset your course database
	python server/data/uclagrades/process21f-22s.py server/data/uclagrades/grades-21f-222.csv
	python server/data/uclagrades/process22f-23s.py server/data/uclagrades/grades-22f-23s.csv
	python server/data/uclagrades/process23f-24s.py server/data/uclagrades/grades-23f-24s.csv
	echo "Grades database loaded successfully."

check: deps
	pytest

clean: deps
	echo "Removing all example courses from database"