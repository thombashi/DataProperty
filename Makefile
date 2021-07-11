AUTHOR := thombashi
PACKAGE := DataProperty
BUILD_WORK_DIR := _work
PKG_BUILD_DIR := $(BUILD_WORK_DIR)/$(PACKAGE)


.PHONY: build-remote
build-remote: clean
	@mkdir -p $(BUILD_WORK_DIR)
	@cd $(BUILD_WORK_DIR) && \
		git clone https://github.com/$(AUTHOR)/$(PACKAGE).git && \
		cd $(PACKAGE) && \
		tox -e build
	ls -lh $(PKG_BUILD_DIR)/dist/*

.PHONY: build
build: clean
	@tox -e build
	ls -lh dist/*

.PHONY: check
check:
	tox -e lint
	travis lint
	pip check

.PHONY: clean
clean:
	@rm -rf $(BUILD_WORK_DIR)
	@tox -e clean

.PHONY: fmt
fmt:
	@tox -e fmt

.PHONY: release
release:
	@cd $(PKG_BUILD_DIR) && python setup.py release --sign --dir dataproperty
	@make clean

.PHONY: setup
setup:
	@pip install --upgrade -e .[test] releasecmd tox
	pip check
