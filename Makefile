.PHONY: run healthcheck


run:
	docker compose -p test --profile enabled up --build --force-recreate

healthcheck:
	python replace_flag.py
