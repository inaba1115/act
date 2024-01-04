.PHONY: lint
lint:
	poetry run black .
	poetry run isort .

.PHONY: test
test:
	poetry run python -m unittest
