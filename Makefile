test:
	python pytranslate/text_utils.py
	python pytranslate/english_model.py
	nosetests -v

eval:
	python pytranslate/evaluation.py

clean:
	rm -f *.pyc
