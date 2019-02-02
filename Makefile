PACKAGE := DataProperty
BUILD_DIR := build


.PHONY: build
build:
	@make clean
	@python setup.py build
	@rm -rf $(BUILD_DIR)/

.PHONY: clean
clean:
	@rm -rf $(PACKAGE)-*.*.*/ \
		$(BUILD_DIR) \
		dist/ \
		.eggs/ \
		.pytest_cache/ \
		.tox/ \
		**/*/__pycache__/ \
		*.egg-info/

.PHONY: fmt
fmt:
	@black $(CURDIR)
	@autoflake --in-place --recursive --remove-all-unused-imports --exclude "__init__.py" .
	@isort --apply --recursive

.PHONY: release
release:
	@python setup.py release --sign
	@rm -rf dist/
