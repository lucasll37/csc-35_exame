.PHONY: clean configure build test help

.DEFAULT_GOAL := help clear env


clean: ## Clean all generated build files in the project.
	rm -rf ./.venv
	rm -rf ./.pytest_cache
	find . -type f -name '*.py[co]' -delete
	find . -type d -name __pycache__ -delete
	@echo "Done."


env: ## Configure the project for building.
	python3 -m venv ./.venv
	bash -c "source ./.venv/bin/activate && \
		pip install -r requirements.txt && \
		pip install --upgrade pip"
	@echo "Done."


help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
