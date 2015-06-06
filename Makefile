help:
	-@ echo "clean  remove build dirs"
	-@ echo "test   run tests"

clean:
	-@ rm -rf build/
	-@ rm -rf dist/
	-@ rm -rf s3_backups.egg-info/

test:
	@echo "Checking code using pep8 ..."
	-@pep8 --ignore E501 .
	@echo "Checking code using pyflakes ..."
	-@pyflakes .
	@echo "Running tests ..."
	-@python s3_backups/tests.py

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
