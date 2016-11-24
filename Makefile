test:
	nosetests -v
	python pytranslate/translator.py

eval:
	python pytranslate/evaluation.py

clean:
	rm -f *.pyc
