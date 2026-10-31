PYTHON = python3
MAIN_FILE = a_maze_ing.py
CONFIG = config.txt
PIP = pip

all: install run

install:
	$(PIP) install flake8
	$(PIP) install mypy

run:
	$(PYTHON) $(MAIN_FILE) $(CONFIG)


debug:
	$(PYTHON) -m pdb $(MAIN_FILE) $(CONFIG)

clean:
	rm -rf __pycache__
	rm -rf .mypy_cache
	rm -rf ./.mypy_cache
	rm -rf */__pycache__

lint:
	flake8
	mypy . \
	--warn-return-any \
	--warn-unused-ignores \
	--ignore-missing-imports \
	--disallow-untyped-defs \
	--check-untyped-defs

.PHONY: all install run debug lint clean