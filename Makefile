release: build
	twine upload dist/*

build:
	python setup.py bdist_wheel

clean:
	rm -rf build release dist whaledo.egg-info

.PHONY: release build clean
