.DEFAULT_GOAL := help
INIT_SCRIPT_PATH := ./setup/init.sh
UPDATE_SCRIPT_PATH := ./setup/update.sh
NOTEBOOKS_DIR := ./notebooks

.PHONY: help
help: ## Show this help message
	@printf "\033[33mUsage:\033[0m\n  make [target] [arg=\"val\"...]\n\n\033[33mTargets:\033[0m\n"
	@grep -E '^[-a-zA-Z0-9_\.\/]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[32m%-15s\033[0m %s\n", $$1, $$2}'

.PHONY: init
init: ## Initialize the project
	@bash $(INIT_SCRIPT_PATH)

.PHONY: clean
clean: ## Clean the Jupyter notebooks
	@echo "Cleaning notebooks..."
	@find $(NOTEBOOKS_DIR) -name '*.ipynb' -print0 | xargs -0 -I {} jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace {}
	@echo "Notebooks cleaned!"

.PHONY: update
update: ## Update the pip dependencies
	@bash $(UPDATE_SCRIPT_PATH)
