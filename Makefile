clean:
	rm -rf dist cosmicpi.egg-info build

publish-test: clean
	python3 setup.py sdist bdist_wheel
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

publish: clean
	python3 setup.py sdist bdist_wheel
	twine upload dist/*

publish-ci:
	# Set environment variables `TWINE_PASSWORD` and `TWINE_USERNAME`
	pip3 install twine --user 
	$(MAKE) publish