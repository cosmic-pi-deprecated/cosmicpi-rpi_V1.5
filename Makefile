publish:
	pip install twine
	python setup.py sdist
	twine upload dist/*

ci-publish:
	echo '[pypi]' > ~/.pypirc
	echo 'username=lukicdarkoo' >> ~/.pypirc
	echo "password=${PYPI_PASSWORD}" >> ~/.pypirc
	$(MAKE) publish