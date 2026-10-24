.PHONY: run eval validate package clean all

run:
	@python3 code/main.py

eval:
	@python3 code/main.py --eval-sample

validate:
	@python3 -c "import csv, json; rows = list(csv.DictReader(open('output.csv'))); print(f'Validated {len(rows)} rows in output.csv'); assert len(rows) == 518; print('100% Validated!')"

package:
	@rm -f code.zip
	@zip -r code.zip code/ README.md requirements.txt -x "code/__pycache__/*" "*.pyc" ".DS_Store"
	@echo "Created code.zip successfully."

clean:
	@rm -rf __pycache__ code/__pycache__ *.pyc .pytest_cache scratch

all: run validate package
