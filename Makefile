SHELL=/bin/bash
LINT_PATHS=chessli/ setup.py

.PHONY: readme all cli
.DEFAULT_GOAL := help
.SILENT: make-commands-overview dependency-structure folder-structure readme

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
docs: readme postprocess-readme ## (Re)create the whole project documentation
	@cp readme.md docs/mkdocs_index.md
	@echo "Finished Documentation :)"

cli: ## Create documentation for the cli at docs/cli.md
	@typer $(project_name)/cli/main.py utils docs --name chessli --output docs/cli.md

readme: cli make-commands-overview dependency-structure folder-structure ## Make readme.md
	{ cat docs/index.md; \
	  cat docs/features.md; \
	  cat docs/getting_started.md; \
	  cat docs/basic_usage.md; \
	  cat docs/acknowledgments.md; \
	} > readme.md

postprocess-readme:
	# @pandoc --toc -s readme.md -t gfm -o readme.md # Postprocess readme
	# @printf "# $(project_name)\n\n" | cat - readme.md > temp && mv temp readme.md

make-commands-overview: 
	  { \
	  printf "## Available make-commands\n"; \
	  printf '```\n'; \
	  make -s help ; \
	  printf '```\n\n' ; \
	  } > docs/make_commands_overview.md

dependency-structure: 
	{ \
	  printf "## Dependency Structure\n\n"; \
	  printf "![Dependency Structure](imgs/$(project_name).svg 'Dependency Structure')\n\n"; \
	} > docs/dependency_structure.md

folder-structure: 
	{ \
	  printf "## Folder Structure\n"; \
	  printf '```\n'; \
	  tree -L 2 -I "*egg*"; \
	  printf '```\n\n'; \
	} > docs/folder_structure.md


pydeps-plot:  ## (Re)create a pydeps-plot and save it in the docs
	@pydeps $(project_name) -o imgs/$(project_name).svg --no-show
	@cp imgs/$(project_name).svg docs/imgs/


################################################################################
#                               Formatting & Co                                #
################################################################################
type:
	pytype -j auto

format:
	# Sort imports
	isort ${LINT_PATHS}
	# Reformat using black
	black -l 88 ${LINT_PATHS}

check-codestyle:
	# Sort imports
	isort --check ${LINT_PATHS}
	# Reformat using black
	black --check -l 88 ${LINT_PATHS}

slow_type=xdotool type --delay 100

demo_intro:
	@toilet --metal "Welcome to CHESSLI"
	@printf "\n\n"
	@$(slow_type) "A free and open-source CHESS improvement program that combines the power of Lichess and Anki."
	@printf "\n"
	@$(slow_type) "Let's see what it can do!"
	@sleep 1 
	@xdotool exec "clear"

demo_games: 
	@toilet --metal "Games"
	@$(slow_type) "Fetch your games from Lichess, analyse your mistakes and import them into Anki to never do them again."
	@sleep 1
	@printf "\n"
	@$(slow_type) ">>> chessli games ankify --since last_week"
	@printf "\n\n"
	@sleep 1
	@chessli --user DrNykterstein games ankify --since last_week
	@sleep 2
	@xdotool exec "clear"

demo_openings:
	@toilet --metal "Openings"
	@printf "\n"
	@$(slow_type) "List all openings you have played on Lichess and import them into Anki to create an opening repertoire."
	@printf "\n"
	@sleep 1
	@$(slow_type) ">>> chessli openings ankify --since last_week"
	@printf "\n\n"
	@sleep 1
	@chessli openings ankify --since last_week
	@sleep 2
	@$(slow_type) ">>> chessli openings ls"
	@printf "\n\n"
	@sleep 1
	@chessli openings ls
	@sleep 3
	@xdotool exec "clear"

demo_tactics:
	@toilet --metal " Tactics"
	@$(slow_type) "Fetch your played Lichess puzzles and create Anki cards for them!"
	@printf "\n"
	@$(slow_type) ">>> chessli --user pwenker tactics ankify"
	@printf "\n\n"
	@sleep 1
	@chessli --user wenpas tactics ankify
	@sleep 2
	@xdotool exec "clear"

demo_more:
	@toilet --metal "Much More"
	@printf "\n\n"
	@echo "Get the current leaderboard or visualize your rating history, etc."
	@$(slow_type) ">>> chessli lichess leaderboard"
	@printf "\n\n"
	@sleep 1
	@chessli lichess leaderboard
	@sleep 2
	@$(slow_type) ">>> chessli lichess leaderboard --blitz"
	@printf "\n\n"
	@sleep 1
	@chessli lichess leaderboard --type blitz
	@sleep 1
	@xdotool exec "clear"

demo: demo_intro demo_games demo_openings demo_tactics demo_more
	@toilet --metal "Chessli"
	@printf "\n\n"
	@$(slow_type) ">>> This is version 0.1, there is a lot more to come! Stay tuned :)"
	@sleep 1
	@echo ""

