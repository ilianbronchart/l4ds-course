SHELL := /bin/bash
LOGFILE := logs/$(shell date +%Y-%m-%d_%H-%M-%S).log
SENDER := ilianbronchart@protonmail.com
RECIPIENT := ilianbronchart@protonmail.com
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
	@echo "  clean           (DANGEROUS) Delete data, csv, reports, logs and docs directories."
	@echo ""

install:
	@echo "Installing dependencies..."; \

	@sudo apt-get update;
	@which curl > /dev/null || (echo "curl is not installed. Installing..." && sudo apt-get install -y curl);
	@which mailx > /dev/null || (echo "mailx is not installed. Installing..." && sudo apt-get install -y mailutils);
	@which virtualenv > /dev/null || (echo "virtualenv is not installed. Installing..." && sudo apt install -y python3-virtualenv);

	@echo "Creating necessary directories..."
	@mkdir -p data csv reports ../docs logs;

	@if [ ! -d ".env" ]; then \
		echo "Virtual environment not found. Creating..."; \
		virtualenv .env; \
	fi

	@echo "Activating virtual environment and installing Python dependencies...";
	@. .env/bin/activate && pip install -r requirements.txt;
	
fetch-data:
	@./scripts/fetch_data.sh 2>&1 | tee -a $(LOGFILE)
	@echo "" >> $(LOGFILE)

transform-data:
	@./scripts/transform_data.sh 2>&1 | tee -a $(LOGFILE)
	@echo "" >> $(LOGFILE)

analyze-data:
	@source .env/bin/activate;
	@python3 scripts/analyze_data.py 2>&1 | tee -a $(LOGFILE)
	@echo "" >> $(LOGFILE)

generate-report:
	@source .env/bin/activate;
	@python3 scripts/generate_report.py 2>&1 | tee -a $(LOGFILE);
	@echo "" >> $(LOGFILE);

run-pipeline: fetch-data transform-data analyze-data generate-report	
	@echo "Pushing pipeline result to remote..." >> $(LOGFILE);
	@git pull >> $(LOGFILE);
	@git add ../docs data >> $(LOGFILE);
	@git commit -m "[AUTOMATIC] Push pipeline result to remote" >> $(LOGFILE);
	@git push >> $(LOGFILE);

	@echo "Sending email with logfile..." >> $(LOGFILE);
	@mail -s "[BikeIndex] Pipeline result on $(date +%Y-%m-%d_%H-%M-%S)" ilianbronchart@gmail.com -A $(LOGFILE) </dev/null;

clean:
	@read -p "Are you sure you want to permanently delete the data, csv, reports, logs and docs directories? [y/N] " confirm; \
	if [ "$$confirm" = "y" ]; then \
		rm -rf reports data csv logs ../docs; \
		echo "Directories deleted."; \
	else \
		echo "Cleanup aborted."; \
	fi

.DEFAULT_GOAL := help	