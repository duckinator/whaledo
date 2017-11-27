release: build
	twine upload dist/*

build:
	python setup.py bdist_wheel

clean:
	rm -rf build release

.PHONY: release build clean
