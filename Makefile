test: clean
	@python test/test_subtitler.py

clean:
	@rm -f *.pyc test/*.pyc

.PHONY: test clean
