REPO_DIR     := $(shell pwd)
HERMES_SKILLS := $(HOME)/.hermes/skills/autonomous-ai-agents
SKILL_NAME   := pi
LINK_PATH    := $(HERMES_SKILLS)/$(SKILL_NAME)
BACKUP_ROOT  := $(HERMES_SKILLS)/.backup

.PHONY: help install link unlink sync verify-sync test lint ci

help: ## Show this help
	@echo "Targets: install link unlink sync verify-sync test lint ci"

install: link ## Alias for link (idempotent symlink installer)

link: ## Backup existing in-Hermes pi dir, then symlink to this checkout
	@./install.sh

unlink: ## Remove the in-Hermes pi symlink (does not delete backup)
	@if [ -L "$(LINK_PATH)" ]; then \
		rm "$(LINK_PATH)"; \
		echo "Removed symlink $(LINK_PATH)"; \
	else \
		echo "No symlink at $(LINK_PATH); nothing to do."; \
	fi

sync: ## Fast-forward this checkout to origin/main
	@git -C "$(REPO_DIR)" fetch origin
	@git -C "$(REPO_DIR)" switch main
	@git -C "$(REPO_DIR)" merge --ff-only origin/main

verify-sync: ## Assert symlink + clean tree + HEAD == origin/main
	@./scripts/verify-sync.sh

test: ## Run pytest via mise
	@mise run test

lint: ## Lint via mise
	@mise run lint

ci: lint verify-sync test ## Local CI pipeline

