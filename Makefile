PYTHON = poetry run python3
PYPROJECT = pyproject.toml
CONFIG = config.txt

all: install lint run

install:
	poetry install
run:
	$(PYTHON) a_maze_ing.py $(CONFIG)
lint:
	poetry run flake8 .
	poetry run mypy .
debug:
	$(PYTHON) -m pdb a_maze_ing.py $(CONFIG)
clean:
	rm -rf __pycache__
	rm -rf .mypy_cache
	rm -rf dist
	rm -rf .pytest_cache
	@echo "Cleanup complete."

.PHONY: all install run lint debug clean
