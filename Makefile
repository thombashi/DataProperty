AUTHOR := thombashi
PACKAGE := DataProperty
BUILD_WORK_DIR := _work
BUILD_PKG_DIR := $(BUILD_WORK_DIR)/$(PACKAGE)


.PHONY: build-remote
build-remote:
	@rm -rf $(BUILD_WORK_DIR)
	@mkdir -p $(BUILD_WORK_DIR)
	@cd $(BUILD_WORK_DIR) && \
		git clone https://github.com/$(AUTHOR)/$(PACKAGE).git && \
		cd $(PACKAGE) && \
		tox -e build
	ls -lh $(BUILD_PKG_DIR)/dist/*

.PHONY: build
build:
	@make clean
	@tox -e build
	ls -lh dist/*

.PHONY: check
check:
	tox -e lint
	travis lint

.PHONY: clean
clean:
	@tox -e clean
	@rm -rf $(BUILD_WORK_DIR)

.PHONY: fmt
fmt:
	@tox -e fmt

.PHONY: release
release:
	@cd $(BUILD_PKG_DIR) && tox -e release
	@make clean

.PHONY: setup
setup:
	@pip install --upgrade -e .[test] tox
