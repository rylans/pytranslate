test:
	python pytranslate/text_utils.py
	nosetests -v
	python pytranslate/translator.py

eval:
	python pytranslate/evaluation.py

clean:
	rm -f *.pyc
