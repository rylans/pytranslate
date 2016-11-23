test:
	nosetests -v

eval:
	python pytranslate/evaluation.py

clean:
	rm -f *.pyc
