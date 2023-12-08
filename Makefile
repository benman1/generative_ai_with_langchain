objects = chat_with_retrieval/ data_science/ information_extraction/ monitoring_and_evaluation/ prompting/ question_answering/ search_engine/ software_development/ summarize/ webserver/ writing_assistant/

typecheck:
	mypy $(objects)

lint:
	flake8 --jobs 4 --statistics --show-source $(objects) 
	# pylint --jobs 4 $(objects)
	black --target-version py36 --skip-string-normalization --check $(objects) 


