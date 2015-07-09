help:
	-@ echo "clean          remove build dirs"
	-@ echo "lint           check the code using pep8 and pyflakes"
	-@ echo "lint_docs      check docs source code"
	-@ echo "test           run tests"
	-@ echo "test_coverage  run tests with coverage"

clean:
	-@ rm -rf build/
	-@ rm -rf dist/
	-@ rm -rf s3_backups.egg-info/

lint:
	@echo "Checking code using pep8 and pyflakes ..."
	@flake8 . --ignore=E501

lint_docs:
	@echo "\nChecking sphinx syntax ..."
	@cd docs/ && sphinx-build -nW -b html -d _build/doctrees . _build/html

test:
	@echo "\nRunning tests ..."
	@python s3_backups/tests.py

test_coverage:
	@echo "\nRunning tests with coverage ..."
	@coverage run s3_backups/tests.py && coverage html && open htmlcov/index.html

backup_postgres:
	-s3_backups/postgres_to_s3.py \
		-v \
		--POSTGRES_DUMP_PATH=$(POSTGRES_DUMP_PATH) \
		--AWS_ACCESS_KEY_ID=$(AWS_ACCESS_KEY_ID) \
		--AWS_SECRET_ACCESS_KEY=$(AWS_SECRET_ACCESS_KEY) \
		--S3_BUCKET_NAME=$(S3_BUCKET_NAME) \
		--S3_KEY_NAME=$(S3_KEY_NAME) \
		--backup

archive_postgres:
	-s3_backups/postgres_to_s3.py \
		-v \
		--POSTGRES_DUMP_PATH=$(POSTGRES_DUMP_PATH) \
		--AWS_ACCESS_KEY_ID=$(AWS_ACCESS_KEY_ID) \
		--AWS_SECRET_ACCESS_KEY=$(AWS_SECRET_ACCESS_KEY) \
		--S3_BUCKET_NAME=$(S3_BUCKET_NAME) \
		--S3_KEY_NAME=$(S3_KEY_NAME) \
		--archive
