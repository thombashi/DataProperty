PACKAGE := DataProperty


.PHONY: build
build:
	@make clean
	@python setup.py sdist bdist_wheel
	@twine check dist/*
	@python setup.py clean --all
	ls -lh dist/*

.PHONY: check
check:
	python setup.py check
	codespell -q2 dataproperty examples test README.rst
	travis lint
	pylama

.PHONY: clean
clean:
	@rm -rf $(PACKAGE)-*.*.*/ \
		dist/ \
		pip-wheel-metadata/ \
		.eggs/ \
		.pytest_cache/ \
		.tox/ \
		**/__pycache__/ \
		**/*/__pycache__/ \
		*.egg-info/
	@python setup.py clean --all
	@find . -not -path '*/\.*' -type f | grep -E .+\.py\.[a-z0-9]{32,}\.py$ | xargs -r rm

.PHONY: fmt
fmt:
	@black $(CURDIR)
	@autoflake --in-place --recursive --remove-all-unused-imports --exclude "__init__.py" .
	@isort --apply --recursive

.PHONY: release
release:
	@python setup.py release --sign
	@make clean

.PHONY: setup
setup:
	@pip install --upgrade .[dev] tox
