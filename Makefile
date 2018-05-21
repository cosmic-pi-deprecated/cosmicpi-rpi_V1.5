clean:
	rm -rf dist cosmicpi.egg-info build

publish: clean
	python setup.py sdist upload

ci-publish:
	echo '[pypi]' > ~/.pypirc
	echo 'username=lukicdarkoo' >> ~/.pypirc
	echo "password=${PYPI_PASSWORD}" >> ~/.pypirc
	$(MAKE) publish