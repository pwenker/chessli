SHELL=/bin/bash
LINT_PATHS=chessli/

.PHONY: readme all cli tests
.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print(f"{target:20} {help}")
endef
export PRINT_HELP_PYSCRIPT

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)


project_name=chessli

################################################################################
#                                    Docs                                      #
################################################################################
docs: readme ## (Re)create the whole project documentation
	@echo "Finished Documentation :)"

cli: ## Create documentation for the cli at docs/cli.md
	@typer $(project_name)/cli/main.py utils docs --name chessli --output docs/cli.md

readme: cli ## Make readme.md
	@{ scripts/strip_yaml_metadata.sh docs/index.md; \
	  scripts/strip_yaml_metadata.sh docs/features.md; \
	  scripts/strip_yaml_metadata.sh docs/getting_started.md; \
	  scripts/strip_yaml_metadata.sh docs/basic_usage.md; \
	  scripts/strip_yaml_metadata.sh docs/acknowledgments.md; \
	} > readme.md

make-commands-overview:
	  { \
	  printf "## Available make-commands\n"; \
	  printf '```\n'; \
	  make -s help ; \
	  printf '```\n\n' ; \
	  } > docs/make_commands_overview.md

################################################################################
#                               Formatting & Testing                           #
################################################################################
tests:  ## Execute all tests
	pytest

ci-tests: ## Execute subset of tests (e.g. ignores slow tests)
	pytest -m "not slow" -vv .

type:
	pytype -j auto

format:
	# Sort imports
	isort --profile black --filter-files ${LINT_PATHS}
	# Reformat using black
	black -l 88 ${LINT_PATHS}

format-check:
	# Sort imports
	isort --check --profile black --filter-files ${LINT_PATHS}
	# Reformat using black
	black --check -l 88 ${LINT_PATHS}

commit-checks: format type
