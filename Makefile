test:
		pytest --cov=lrg_omics --cov-report html
	    coverage-badge -o images/coverage.svg

docs:
		mkdocs build && mkdocs gh-deploy

format:
	black .
	
deploy:
	rm dist/*
	python setup.py sdist bdist_wheel
	python -m twine upload --repository lrg-omics dist/lrg*omics-*
