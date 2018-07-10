LINE_WHERE_TO_INSERT=123

.PHONY: docs

all: docs

docs:
	sed -e "$(LINE_WHERE_TO_INSERT)r slides.md" remarkjs_boilerplate.html > index.html
