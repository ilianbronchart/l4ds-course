.PHONY: help

help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@echo "  check-venv      Check if virtual environment exists and create if necessary"
	@echo "  check-curl      Check if curl is installed and install if necessary"
	@echo "  fetch-data      Fetch data from remote server"
	@echo "  transform-data  Transform data into CSV format"
	@echo "  analyze-data    Analyze data and generate report data"
	@echo "  generate-report Generate report from analyzed data"
	@echo "  clean           (DANGEROUS) Delete reports, data, csv, docs and .env directories"
	@echo ""

check-venv:
	@if [ ! -d ".env" ]; then \
		echo "Virtual environment not found. Creating..."; \
		python3 -m venv .env; \
		source .env/bin/activate; \
		pip install -r requirements.txt; \
	fi

check-curl:
	@which curl > /dev/null || (echo "curl is not installed. Installing..." && sudo apt-get update && sudo apt-get install -y curl)

install: check-venv check-curl

fetch-data:
	./fetch-data.sh

transform-data:
	./transform-data.sh

analyze-data:
	python analyze-data.py

generate-report:
	python generate-report.py

run-pipeline: install fetch-data transform-data analyze-data generate-report

clean:
	@read -p "Are you sure you want to delete the reports, data, csv, and .env directories? [y/N] " confirm; \
	if [ "$$confirm" = "y" ]; then \
		rm -rf reports data csv .env ../docs; \
		echo "Directories deleted."; \
	else \
		echo "Cleanup aborted."; \
	fi

.DEFAULT_GOAL := help