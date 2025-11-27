setup:
	pip install -r requirements.txt

run:
	python src/run.py "Analyze ROAS drop"

test:
	pytest tests/

lint:
	pylint src/

# End of Makefile
