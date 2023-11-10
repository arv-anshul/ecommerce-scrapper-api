.ONESHELL:

.DEFAULT_GOAL := run

run:
	uvicorn --reload ecommerce.api.app:app

.PHONY: test
test: ecommerce/tests/
	pytest $<
