help:
	-@ echo "clean  remove build dirs"
	-@ echo "test   run tests"

clean:
	-@ rm -rf build/
	-@ rm -rf dist/
	-@ rm -rf s3_backups.egg-info/

test:
	-flake8 s3_backups --ignore=E501,E128,W404,F403
	-python s3_backups/tests.py