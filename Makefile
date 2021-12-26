install: 
	poetry install

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --user --force-reinstall dist/*.whl

lint:
	poetry run flake8 page_loader

pytest:
	poetry run pytest
	
test-coverage:
	poetry run pytest --cov=page_loader --cov-report xml