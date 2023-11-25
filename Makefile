DEFAULT_TARGET = .

lint:
	flake8 app/
	isort -q --check app/
	black -q --check app/

format:
	isort -q app/
	black -q app/

type_check:
	mypy app/

run:
	streamlit run app/main.py --server.port 8080
