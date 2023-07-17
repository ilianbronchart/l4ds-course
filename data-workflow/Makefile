SHELL := /bin/bash
.PHONY: help

help:
	@echo "Usage: make <target>"
	@echo "Targets:"
	@echo "  install         Install dependencies"
	@echo "  run-pipeline    Run the entire pipeline from start to finish."
	@echo "  fetch-data      Fetch data from remote server"
	@echo "  transform-data  Transform data into CSV format"
	@echo "  analyze-data    Analyze data and generate report files"
	@echo "  generate-report Generate report from analyzed data"
	@echo "  clean           (DANGEROUS) Delete data, csv, reports and docs directories."
	@echo ""

install:
	@echo "Installing dependencies..."; \

	@if [ ! -d ".env" ]; then \
		echo "Virtual environment not found. Creating..."; \
		python3 -m venv .env; \
	fi
	@ source .env/bin/activate; \
	@echo "Installing Python dependencies..."; \
	pip install -r requirements.txt; \

	@ which curl > /dev/null || (echo "curl is not installed. Installing..." && sudo apt-get update && sudo apt-get install -y curl);
	
fetch-data:
	@echo "Fetching data from remote..."; \
	./scripts/fetch_data.sh

transform-data:
	@echo "Transforming data into CSV format..."; \
	./scripts/transform_data.sh

analyze-data:
	@echo "Analyzing data and generating report files..."; \
	source .env/bin/activate; \
	python3 scripts/analyze_data.py

generate-report:
	@echo "Generating report from analyzed data..."; \
	source .env/bin/activate; \
	python3 scripts/generate_report.py

run-pipeline: fetch-data transform-data analyze-data generate-report	
	@ echo "Pushing pipeline result to remote...";
	@ git add ../docs data csv reports;
	@ git commit -m "[AUTOMATIC] Push pipeline result to remote";
	@ git push;

clean:
	@read -p "Are you sure you want to permanently delete the data, csv, reports and docs directories? [y/N] " confirm; \
	if [ "$$confirm" = "y" ]; then \
		rm -rf reports data csv ../docs; \
		echo "Directories deleted."; \
	else \
		echo "Cleanup aborted."; \
	fi

.DEFAULT_GOAL := help