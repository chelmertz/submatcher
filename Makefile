test: clean
	@python test/test_submatcher.py

install_dev: clean
	@pip install -e .

package: clean
	@python setup.py sdist

clean:
	@rm -f *.pyc test/*.pyc

.PHONY: test clean package install
