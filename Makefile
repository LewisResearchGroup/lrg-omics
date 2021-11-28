test:
		pytest --cov=lrg_omics --cov-report html
	    coverage-badge -o images/coverage.svg

docs:
		mkdocs build && mkdocs gh-deploy

format:
	black .