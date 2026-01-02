lang ?= "en"

help:
	@echo "available options:"
	@echo -e "  start - runs the application"
	@echo -e "  changelang lang={language_code} - changes the interface language"
	@echo


start:
	@python main.py

changelang:
	@echo 'lang = "${lang}"' > init.py
