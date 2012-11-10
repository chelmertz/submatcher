test: clean
	@python test/test_subtitler.py

install: clean
	@python setup.py install

package: clean
	@python setup.py sdist

clean:
	@rm -f *.pyc test/*.pyc

.PHONY: test clean package install
