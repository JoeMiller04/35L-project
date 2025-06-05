.PHONY: deps load-db check clean setup-env start start-server start-client

deps:
	pip install -r server/requirements.txt --quiet

load-db: deps
# This will reset your course database
	python server/data/uclagrades/process21f-22s.py server/data/uclagrades/grades-21f-222.csv
	python server/data/uclagrades/process22f-23s.py server/data/uclagrades/grades-22f-23s.csv
	python server/data/uclagrades/process23f-24s.py server/data/uclagrades/grades-23f-24s.csv
	@echo "Grades database loaded successfully."
# This will reset your course descriptions database
	python server/data/Kyle/load_descriptions.py server/data/Kyle/35L-project.descriptions.json --drop
# This will reset your course ratings database
	python server/data/bruinwalk_reviews/bruinwalk_connect_to_database.py server/data/bruinwalk_reviews/course_reviews.txt
	python server/data/bruinwalk_reviews/professor_reviews_database.py server/data/bruinwalk_reviews/professor_reviews.txt

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
	python server/data/clean_db.py

start-server: deps setup-env
	uvicorn server.main:app --reload

start-client:
	cd client && npm install && npm start

start: deps setup-env
	@echo "Starting both server and client..."
	@echo "Use Ctrl+C to stop both processes"
	@(trap 'kill 0' SIGINT; \
		$(MAKE) start-server & \
		$(MAKE) start-client & \
		wait)